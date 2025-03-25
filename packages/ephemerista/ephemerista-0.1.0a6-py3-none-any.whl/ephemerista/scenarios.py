"""The scenarios.py module.

This module provides the `Scenario` class which collects all required inputs such as assets, communications channels,
points and areas of interest for orbit propagation and analyses.
"""

import os
from pathlib import Path
from typing import Self
from uuid import uuid4

import geopandas as gpd
import lox_space as lox
import numpy as np
import pyproj
from geojson_pydantic import Feature, Point, Polygon  # type: ignore
from pydantic import UUID4, Field, PrivateAttr
from shapely import Point as ShapelyPoint
from shapely.ops import transform

from ephemerista import BaseModel
from ephemerista.angles import Angle
from ephemerista.assets import Asset, AssetKey, GroundPoint, _asset_id
from ephemerista.bodies import Origin
from ephemerista.comms.channels import Channel
from ephemerista.coords.trajectories import Trajectory
from ephemerista.coords.twobody import DEFAULT_FRAME, DEFAULT_ORIGIN
from ephemerista.frames import ReferenceFrame
from ephemerista.propagators.orekit.conversions import time_to_abs_date
from ephemerista.time import Time


def _earth_rotation(time: Time):
    from org.orekit.bodies import CelestialBodyFactory  # type: ignore
    from org.orekit.frames import FramesFactory  # type: ignore

    icrf = FramesFactory.getICRF()
    body_fixed = CelestialBodyFactory.getEarth().getBodyOrientedFrame()
    return icrf.getTransformTo(body_fixed, time_to_abs_date(time)).getRotation()


class Ensemble(BaseModel):
    """The `Ensemble` model.

    This class collects the resulting trajectories from propagating the state of all assets within a scenario.
    """

    trajectories: dict[UUID4, Trajectory] = Field(description="Dictionary of trajectories indexed by asset IDs")
    ephemerides: dict[str, Trajectory] = Field(default={})
    _ensemble: lox.Ensemble = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._ensemble = lox.Ensemble(
            {str(uuid): trajectory._trajectory for uuid, trajectory in self.trajectories.items()}
        )

    def __getitem__(self, asset: AssetKey) -> Trajectory:
        """Return the trajectory for a given asset."""
        return self.trajectories[_asset_id(asset)]

    def add_earth_attitude(self):
        """Add attitude quaternions for Earth to the ensemble."""
        if not self.trajectories:
            return
        trajectory = next(iter(self.trajectories.values()))
        n = len(trajectory.simulation_time)
        states = np.zeros((n, 7))
        states[:, 0] = trajectory.simulation_time
        rotations = [_earth_rotation(t) for t in trajectory.times]
        attitude = [(rot.getQ0(), rot.getQ1(), rot.getQ2(), rot.getQ3()) for rot in rotations]

        self.ephemerides["earth"] = Trajectory(
            trajectory_type="ephemeris", start_time=trajectory.times[0], states=states, attitude=attitude
        )


class Scenario(BaseModel):
    """The `Scenario` model."""

    scenario_id: UUID4 = Field(alias="id", default_factory=uuid4, description="Scenario ID")
    name: str = Field(description="The name of the scenario", default="Scenario")
    start_time: Time = Field(description="Start time of the scenario")
    end_time: Time = Field(description="End time of the scenario")
    time_step: float = Field(default=60, description="Time step in seconds")
    origin: Origin = Field(
        default=DEFAULT_ORIGIN,
        description="Origin of the coordinate system",
    )
    frame: ReferenceFrame = Field(default=DEFAULT_FRAME, description="Reference frame of the coordinate system")
    assets: list[Asset] = Field(default=[], description="List of assets")
    channels: list[Channel] = Field(default=[], description="List of RF channels")
    points_of_interest: list[Feature[Point, dict]] = Field(default=[], description="List of points of interest")
    areas_of_interest: list[Feature[Polygon, dict]] = Field(default=[], description="List of areas of interest")

    def __init__(self, **data):
        super().__init__(**data)
        self._gen_points_from_aoi()

    def _gen_points_from_aoi(self):
        # Add GroundPoint Assets to the propagator, representing the exterior points of the polygons
        # defined by the scenario's areas_of_interest.
        # In a grid represented by adjacent polygons, points are shared between multiple polygons,
        # therefore to avoid duplicate ground points (and thus extra computations), we do the following:
        #   - identify which points are shared between polygons
        #   - only keep one point but keep track of all polygons this point belongs to
        delta_m_max = 1.0  # distance threshold in meters to decide if a point belongs to a polygon's exterior

        wgs84 = pyproj.CRS("EPSG:4326")
        mercator = pyproj.CRS("EPSG:3857")
        project = pyproj.Transformer.from_crs(wgs84, mercator, always_xy=True).transform

        gdf = gpd.GeoDataFrame(columns=["geometry", "ground_point"], crs="EPSG:3857")  # type: ignore
        u_point_id = 0

        for polygon_id in range(0, len(self.areas_of_interest)):
            polygon = self.areas_of_interest[polygon_id]
            geometry = polygon.geometry
            exterior = geometry.exterior  # type: ignore
            self.areas_of_interest[polygon_id].properties["polygon_id"] = polygon_id  # type: ignore
            # Omitting the last point which is the same as the first point
            n_points = len(exterior) - 1  # type: ignore
            self.areas_of_interest[polygon_id].properties["n_exterior_points"] = n_points  # type: ignore
            min_elevation_deg = self.areas_of_interest[polygon_id].properties.get("min_elevation_deg", 0.0)  # type: ignore

            for point_id in range(0, n_points):
                point = exterior[point_id]  # type: ignore
                shapely_point = transform(project, ShapelyPoint(point.longitude, point.latitude))

                u_point_id_match = 0
                within_distance = False
                if len(gdf) > 0:
                    distances = gdf.distance(shapely_point)
                    u_point_id_match = distances.idxmin()
                    within_distance = distances[u_point_id_match] < delta_m_max

                if within_distance:
                    # we found an existing polygon point within distance threshold
                    gdf.loc[u_point_id_match, "ground_point"].polygon_ids.append(polygon_id)  # type: ignore
                else:
                    gdf.loc[u_point_id] = [
                        shapely_point,
                        GroundPoint.from_lla(
                            latitude=point.latitude,
                            longitude=point.longitude,
                            polygon_ids=[polygon_id],
                            minimum_elevation=Angle.from_degrees(min_elevation_deg),
                        ),
                    ]
                    u_point_id += 1
        for polygon_root_id, points_data in gdf.iterrows():
            self.assets.append(
                Asset(
                    model=points_data["ground_point"],
                    name=f"polygon_{polygon_root_id}",
                )
            )

    @classmethod
    def load_from_file(cls, path: str | os.PathLike) -> Self:
        """Load a scenario from a JSON file."""
        json = Path(path).read_text()
        return cls.model_validate_json(json)

    def _get_asset(self, asset: AssetKey | str) -> Asset | None:
        if isinstance(asset, str):
            return next((a for a in self.assets if a.name == asset), None)
        return next((a for a in self.assets if a.asset_id == _asset_id(asset)), None)

    def __getitem__(self, key: AssetKey | str) -> Asset:
        """Look up an asset based on its name or UUID."""
        asset = self._get_asset(key)
        if not asset:
            raise KeyError()
        return asset

    def channel_by_id(self, channel_id: UUID4) -> Channel:
        """Look up a communications channel based on its UUID."""
        return next(c for c in self.channels if c.channel_id == channel_id)

    @property
    def times(self) -> list[Time]:
        """list[Time]: Time steps."""
        return self.start_time.trange(self.end_time, self.time_step)

    def propagate(self) -> Ensemble:
        """Propagate the state of all assets in the scenario.

        Returns
        -------
        Ensemble
            A collection of all propagated trajectories
        """
        trajectories = {asset.asset_id: asset.model.propagate(self.times) for asset in self.assets}
        return Ensemble(trajectories=trajectories)
