"""The coverage.py module.

This module provides the `Coverage` class for conducting coverage analyses.
"""

from pathlib import Path

import antimeridian
import geopandas as gpd
import h3
import numpy as np
import pandas as pd
import plotly.express as px
from geojson_pydantic import Feature, FeatureCollection
from geojson_pydantic import Polygon as PolygonPydantic
from lox_space import TimeDelta
from matplotlib.axes import Axes
from plotly.graph_objs import Figure
from pydantic import Field
from shapely import MultiPolygon, Polygon

from ephemerista import BaseModel
from ephemerista.analysis import Analysis
from ephemerista.analysis.visibility import Visibility, VisibilityResults
from ephemerista.assets import GroundPoint, Spacecraft
from ephemerista.scenarios import Ensemble, Scenario
from ephemerista.time import Time

PolygonFeature = Feature[PolygonPydantic, dict]
PolygonFeatureCollection = FeatureCollection[PolygonFeature]


def polygonize_aoi(aoi_geom_dict: dict, res: int, min_elevation_deg: float = 0.0) -> list[PolygonFeature]:
    """
    Polygonize an area of interest using h3.

    Parameters
    ----------
    aoi: dict
        A GeoJSON-compatible dict containing a "coordinates" key, usually from a __geo_interface__
    res: int
        h3 res parameter
    min_elevation_deg: float
        Minimum elevation in degrees to compute the visibility between a spacecraft and the ground cells
    """
    cell_list = h3.geo_to_cells(aoi_geom_dict, res=res)

    feature_list = []
    geometry = []
    for cell in cell_list:
        boundary = h3.cell_to_boundary(cell)
        lon_lat_tuples = []
        for bound_coords in boundary:
            lon_lat_tuples.append((bound_coords[1], bound_coords[0]))
        polygon = Polygon(lon_lat_tuples)
        poly_or_multipoly = antimeridian.fix_polygon(polygon)
        geometry.append(poly_or_multipoly)
        if isinstance(
            poly_or_multipoly, MultiPolygon
        ):  # antimeridian sometimes has to split a polygon and returns a MultiPolygon instead
            for poly in poly_or_multipoly.geoms:
                feature_list.append(
                    PolygonFeature(geometry=poly, properties={"min_elevation_deg": min_elevation_deg}, type="Feature")  # type: ignore
                )
        else:
            feature_list.append(
                PolygonFeature(
                    geometry=poly_or_multipoly,  # type: ignore
                    properties={"min_elevation_deg": min_elevation_deg},
                    type="Feature",
                )
            )

    return feature_list


def load_geojson_multipolygon(filename: Path | str, min_elevation_deg: float = 0.0) -> list[PolygonFeature]:
    """
    Load polygons from a GeoJSON file.

    Parameters
    ----------
    min_elevation_deg: float
        Minimum elevation in degrees to compute the visibility between a spacecraft and the ground locations
    """
    with open(filename) as f:
        json_str = f.read()

    model = PolygonFeatureCollection.model_validate_json(json_str)
    feature_list = []
    for feature in model.features:
        properties = feature.properties
        if properties:
            properties["min_elevation_deg"] = min_elevation_deg
        feature_list.append(feature.model_copy(update={"properties": properties}))

    return feature_list


def _merge_time_intervals(intervals_df: pd.DataFrame) -> pd.DataFrame:
    if len(intervals_df) <= 1:
        return intervals_df

    dt_merge = 1000.0

    intervals_df = intervals_df.sort_values("START")
    intervals_df.reset_index(drop=True, inplace=True)

    # Artificially extended the passes by 1000 seconds for grouping
    # to avoid adjacent cells to see wrongly two passes which were close but still disjoint
    intervals_df["START_EXTENDED"] = intervals_df["START"] - dt_merge
    intervals_df["FINISH_EXTENDED"] = intervals_df["FINISH"] + dt_merge

    intervals_df["group"] = (intervals_df["START_EXTENDED"] > intervals_df["FINISH_EXTENDED"].shift().cummax()).cumsum()
    df_out = intervals_df.groupby("group").agg({"START_EXTENDED": "min", "FINISH_EXTENDED": "max"})

    df_out["START"] = df_out["START_EXTENDED"] + dt_merge
    df_out["FINISH"] = df_out["FINISH_EXTENDED"] - dt_merge
    return df_out.drop(["START_EXTENDED", "FINISH_EXTENDED"], axis="columns")


class CoverageResults(BaseModel):
    """Results of the `CoverageAnalysis`."""

    polygons: list[PolygonFeature] = Field(description="List of polygons for which the coverage is computed")
    coverage_percent: list[float] = Field(description="Coverage metric for each polygon, between 0 and 1")
    max_time_gaps: list[float] = Field(description="Maximum time gap in days between successive hits, for each polygon")
    revisit_times: list[list[tuple[Time, Time]]] = Field(description="A list of (AOS, LOS) pass times for each polygon")

    def plot_mpl(self, data_to_plot: str = "coverage_percent", legend: bool = True, **kwargs) -> Axes:  # noqa: FBT001, FBT002
        """Plot the coverage results using Matplotlib."""
        geo_df = self.to_geodataframe()
        if data_to_plot not in geo_df:
            msg = f"Column '{data_to_plot}' does not exist"
            raise ValueError(msg)

        ax = geo_df.plot(column=data_to_plot, legend_kwds={"label": data_to_plot}, legend=legend, **kwargs)
        ax.set_ylabel("Longitude [°]")
        ax.set_xlabel("Latitude [°]")
        return ax

    def plot_plotly(
        self,
        data_to_plot: str = "coverage_percent",
        mapbox_style: str = "open-street-map",
        zoom: int = 0,
        opacity: float = 0.7,
        **kwargs,
    ) -> Figure:
        """Plot the coverage results using Plotly."""
        geo_df = self.to_geodataframe()
        if data_to_plot not in geo_df:
            msg = f"Column '{data_to_plot}' does not exist"
            raise ValueError(msg)

        fig = px.choropleth_mapbox(
            geo_df,
            geojson=geo_df.geometry,
            locations=geo_df.index,
            color=data_to_plot,
            mapbox_style=mapbox_style,
            zoom=zoom,
            opacity=opacity,
            **kwargs,
        )
        return fig

    def to_geodataframe(self) -> gpd.GeoDataFrame:
        """Convert to a `GeoDataFrame`."""
        gdf = gpd.GeoDataFrame.from_features(self.polygons)
        gdf["coverage_percent"] = self.coverage_percent
        gdf["max_time_gaps"] = self.max_time_gaps
        gdf["revisit_times"] = self.revisit_times
        return gdf


class Coverage(Analysis[CoverageResults]):
    """Coverage analysis.

    Notes
    -----
    The coverage is computed by computing all passes of the spacecraft over all points of the exterior of each polygon,
    i.e. the visibility from the min elevation defined in the polygon's properties.

    Doing that for all points of the exterior of each polygon is computationally intensive, but that allows to do an
    average of the coverage on the polygon. Besides, when the GroundPoints are created in scenarios.py,
    shared points between adjacent polygons are merged to avoid duplicate computations.

    For instance for a polygon's exterior composed of 4 points, if two points have spacecraft visibility for a total
    duration of 340 seconds, and the two other points for 360 seconds, then the average visibility duration of this
    polygon will be 350 seconds.
    """

    scenario: Scenario = Field(description="The scenario used to analyze the coverage")
    start_time: Time | None = Field(
        default=None, description="Start time (optional, if None the scenario's start time is used)"
    )
    end_time: Time | None = Field(
        default=None, description="End time (optional, if None the scenario's end time is used)"
    )

    def analyze(  # type: ignore
        self,
        ensemble: Ensemble | None = None,
        visibility: VisibilityResults | None = None,
    ) -> CoverageResults:
        """Run the coverage analysis."""
        if not ensemble:
            ensemble = self.scenario.propagate()

        if not visibility:
            visibility = Visibility(scenario=self.scenario, start_time=self.start_time, end_time=self.end_time).analyze(
                ensemble
            )

        ts = self.scenario.start_time
        te = self.scenario.end_time
        scenario_duration = (te - ts).to_decimal_seconds()

        # initialize result struct
        total_covered_time = np.zeros(len(self.scenario.areas_of_interest))
        revisit_times = [[] for _ in range(0, len(self.scenario.areas_of_interest))]
        max_time_gaps = [np.inf for _ in range(0, len(self.scenario.areas_of_interest))]

        ground_point_intervals_dict = {
            asset.asset_id: [] for asset in self.scenario.assets if isinstance(asset.model, GroundPoint)
        }

        for target_id, observers in visibility.passes.items():
            target = self.scenario[target_id]
            if not isinstance(target.model, Spacecraft):
                continue

            for observer_id, passes in observers.items():
                observer = self.scenario[observer_id]
                if not isinstance(observer.model, GroundPoint):
                    continue

                for gs_pass in passes:
                    t0 = gs_pass.window.start
                    t0_rel = (t0 - ts).to_decimal_seconds()  # TODO: try to do the same computation with Time objects
                    t1 = gs_pass.window.stop
                    t1_rel = (t1 - ts).to_decimal_seconds()
                    ground_point_intervals_dict[observer_id].append([t0_rel, t1_rel])

        poly_intervals_df_list = [
            pd.DataFrame(columns=["START", "FINISH"]) for _ in range(0, len(self.scenario.areas_of_interest))
        ]
        for observer_id, intervals in ground_point_intervals_dict.items():
            # Sorting and merging time intervals from all spacecrafts for a given ground point, based on https://stackoverflow.com/a/65282946

            merged_intervals_df = _merge_time_intervals(
                pd.DataFrame.from_records(intervals, columns=["START", "FINISH"])
            )
            merged_intervals_df["duration"] = merged_intervals_df["FINISH"] - merged_intervals_df["START"]
            total_duration_ground_point = merged_intervals_df["duration"].sum()

            ground_point = self.scenario[observer_id].model
            for polygon_id in ground_point.polygon_ids:  # type: ignore
                # Iterating over all the polygons this ground point belongs to
                n_polygon_points = self.scenario.areas_of_interest[polygon_id].properties["n_exterior_points"]  # type: ignore
                total_covered_time[polygon_id] += total_duration_ground_point / n_polygon_points

                if not merged_intervals_df.empty:
                    if poly_intervals_df_list[polygon_id].empty:
                        poly_intervals_df_list[polygon_id] = merged_intervals_df.copy()
                    else:
                        poly_intervals_df_list[polygon_id] = pd.concat(
                            [poly_intervals_df_list[polygon_id], merged_intervals_df], ignore_index=True
                        )

        for polygon_id in range(0, len(self.scenario.areas_of_interest)):
            poly_intervals_df = poly_intervals_df_list[polygon_id]
            if poly_intervals_df.empty:
                continue

            # Sorting and merging time intervals from all spacecrafts for a given polygon, based on https://stackoverflow.com/a/65282946
            poly_intervals_merged_df = _merge_time_intervals(poly_intervals_df[["START", "FINISH"]])

            gap_worst = -np.inf
            for i in range(0, len(poly_intervals_merged_df)):
                # Converting the relative times in seconds back to Time objects
                aos_time = ts + TimeDelta.from_minutes(poly_intervals_merged_df.iloc[i]["START"] / 60)
                los_time = ts + TimeDelta.from_minutes(poly_intervals_merged_df.iloc[i]["FINISH"] / 60)
                revisit_times[polygon_id].append((aos_time, los_time))

                if i < len(poly_intervals_merged_df) - 1:
                    # Computing the gaps between passes
                    gap_s = poly_intervals_merged_df.iloc[i + 1]["START"] - poly_intervals_merged_df.iloc[i]["FINISH"]
                    gap_worst = max(gap_s, gap_worst)

            if np.isinf(gap_worst):
                # If there was only one pass, gap_worst will still be -np.inf;
                # We replace it by scenario_duration
                gap_worst = scenario_duration

            max_time_gaps[polygon_id] = gap_worst / 86400  # Converting to days

        coverage_percentages = total_covered_time / scenario_duration

        return CoverageResults(
            polygons=self.scenario.areas_of_interest,
            coverage_percent=coverage_percentages.tolist(),
            max_time_gaps=max_time_gaps,
            revisit_times=revisit_times,
        )
