"""The visibility.py module.

This module provides the `Visibility` class for conducting visibility analyses.
"""

from itertools import product
from typing import Literal, Self

import lox_space as lox
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from pydantic import UUID4, Field, PrivateAttr, computed_field

from ephemerista import BaseModel, ephemeris, get_eop_provider
from ephemerista.analysis import Analysis
from ephemerista.angles import Angle
from ephemerista.assets import GroundStation, Observables, Spacecraft, _asset_id
from ephemerista.bodies import Origin
from ephemerista.ipy_widgets import with_plot_display_widget
from ephemerista.scenarios import AssetKey, Ensemble, Scenario
from ephemerista.time import Time


class Window(BaseModel):
    """The `Window` class.

    This class models a visibility window.
    """

    start: Time = Field(description="Start time of the window.")
    stop: Time = Field(description="End time of the window.")

    @classmethod
    def _from_lox(cls, window: lox.Window) -> Self:
        return cls(start=Time._from_lox(window.start()), stop=Time._from_lox(window.end()))

    @computed_field
    @property
    def duration(self) -> float:
        """float: duration of the window in seconds."""
        return float(self.stop - self.start)


class Pass(BaseModel):
    """The `Pass` class.

    This class models a ground station pass and provides modelled observables.
    """

    window: Window = Field(description="The visibility window.")
    times: list[Time] = Field(description="Time steps for observables.")
    observables: list[Observables] = Field(description="Observables.")
    _range: lox.Series = PrivateAttr()
    _range_rate: lox.Series = PrivateAttr()
    _azimuth: lox.Series = PrivateAttr()
    _elevation: lox.Series = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        t = [float(t - self.window.start) for t in self.times]
        self._range = lox.Series(t, [obs.rng for obs in self.observables])
        self._range_rate = lox.Series(t, [obs.rng_rate for obs in self.observables])
        self._azimuth = lox.Series(t, [obs.azimuth.radians for obs in self.observables])
        self._elevation = lox.Series(t, [obs.elevation.radians for obs in self.observables])

    def interpolate(self, time: Time) -> Observables:
        """Interpolate observables for a given time within the window."""
        t = float(time - self.window.start)
        return Observables(
            azimuth=Angle.from_radians(self._azimuth.interpolate(t)),
            elevation=Angle.from_radians(self._elevation.interpolate(t)),
            rng=self._range.interpolate(t),
            rng_rate=self._range_rate.interpolate(t),
        )

    def plot(self):
        """Plot the observables."""
        dts = [t.datetime for t in self.times]
        rng = [obs.rng for obs in self.observables]
        rng_rate = [obs.rng_rate for obs in self.observables]
        azimuth = [obs.azimuth.degrees for obs in self.observables]
        elevation = [obs.elevation.degrees for obs in self.observables]

        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        plt.subplots_adjust(hspace=0.3)

        fig.suptitle(f"Pass from {self.window.start.to_utc()} to {self.window.stop.to_utc()}")

        for a in ax.flat:
            a.xaxis.set_major_locator(mdates.HourLocator())
            a.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            a.xaxis.set_tick_params(rotation=45)
            a.grid()

        ax[0, 0].plot(dts, rng)
        ax[0, 0].set_title("Range")
        ax[0, 0].set_ylabel("km")

        ax[0, 1].plot(dts, rng_rate)
        ax[0, 1].set_title("Range Rate")
        ax[0, 1].set_ylabel("km/s")

        ax[1, 0].plot(dts, azimuth)
        ax[1, 0].set_title("Azimuth")
        ax[1, 0].set_ylabel("degrees")

        ax[1, 1].plot(dts, elevation)
        ax[1, 1].set_title("Elevation")
        ax[1, 1].set_ylabel("degrees")
        return fig


@with_plot_display_widget
class VisibilityResults(BaseModel):
    """Results of the `Visibility` analysis."""

    results_type: Literal["visibility"] = Field(default="visibility", frozen=True, repr=False, alias="type")
    passes: dict[UUID4, dict[UUID4, list[Pass]]]
    scenario: Scenario

    # Used by the ipywidget to be able to support flexible plotting
    _widget_data_field: str = "passes"

    def get(self, observer: AssetKey, target: AssetKey) -> list[Pass]:
        """Return all passes for a given observer and target combination."""
        target_passes = self.passes.get(_asset_id(target), {})
        return target_passes.get(_asset_id(observer), [])

    def __getitem__(self, key: tuple[AssetKey, AssetKey]) -> list[Pass]:
        """Return all passes for a given observer and target combination."""
        return self.get(*key)

    def total_duration(self, observer: AssetKey, target: AssetKey) -> float:
        """Return the sum of all visibility durations for a given observer and target combination."""
        return sum(p.window.duration for p in self.get(observer, target))

    def to_dataframe(self, observer: AssetKey, target: AssetKey) -> pd.DataFrame:
        """Convert the results to a Pandas data frame."""
        passes = self.get(observer, target)
        data = []
        for p in passes:
            data.append(
                {
                    "start": p.window.start.datetime,
                    "end": p.window.stop.datetime,
                    "duration": p.window.duration,
                }
            )

        return pd.DataFrame(data)


class Visibility(Analysis[VisibilityResults]):
    """The `Visibility` analysis.

    This analysis finds windows of visibility between ground stations and spacecraft within the provided scenario.
    """

    scenario: Scenario
    start_time: Time | None = Field(default=None)
    end_time: Time | None = Field(default=None)
    bodies: list[Origin] = Field(default=[])

    def analyze(  # type: ignore
        self,
        ensemble: Ensemble | None = None,
    ) -> VisibilityResults:
        """Run the analysis."""
        if not ensemble:
            ensemble = self.scenario.propagate()

        start_time = self.start_time or self.scenario.start_time
        end_time = self.end_time or self.scenario.end_time

        times = [time._time for time in start_time.trange(end_time, self.scenario.time_step)]

        bodies = [body._origin for body in self.bodies]

        passes: dict[UUID4, dict[UUID4, list[Pass]]] = {}

        for observer, target in product(self.scenario.assets, self.scenario.assets):
            if observer == target:
                continue

            if not isinstance(observer.model, GroundStation) or not isinstance(target.model, Spacecraft):
                continue

            observer_id = observer.asset_id
            observer_model = observer.model
            mask = lox.ElevationMask.fixed(observer_model.minimum_elevation.radians)

            target_id = target.asset_id
            target_trajectory = ensemble[target]

            windows = lox.visibility(
                times,
                observer_model._location,
                mask,
                target_trajectory._trajectory,
                ephemeris(),
                bodies,
                get_eop_provider(),
            )

            if target_id not in passes:
                passes[target_id] = {}

            passes[target_id][observer_id] = []

            for w in windows:
                window = Window._from_lox(w)
                if window.stop == window.start:
                    continue
                pass_times = window.start.trange(window.stop, self.scenario.time_step)
                observables = [observer_model.observables(target_trajectory.interpolate(time)) for time in pass_times]
                passes[target_id][observer_id].append(Pass(window=window, times=pass_times, observables=observables))

        return VisibilityResults(passes=passes, scenario=self.scenario)
