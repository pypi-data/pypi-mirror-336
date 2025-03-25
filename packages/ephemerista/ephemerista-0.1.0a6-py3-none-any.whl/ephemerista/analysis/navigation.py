"""The navigation.py module.

This module provides the `Navigation` class.
"""

import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from pydantic import UUID4, Field, computed_field

from ephemerista import BaseModel
from ephemerista.analysis import Analysis
from ephemerista.assets import GroundStation, Spacecraft
from ephemerista.propagators.orekit.conversions import time_to_abs_date, trajectory_to_ephemeris
from ephemerista.scenarios import Ensemble, Scenario
from ephemerista.time import Time


class DilutionOfPrecision(BaseModel):
    """The `DilutionOfPrecision` class.

    This class models the dilution of precision for GNSS satellite constellation at a specific time.
    """

    time: Time
    n_sats: int
    gdop: float
    hdop: float
    pdop: float
    tdop: float
    vdop: float

    @classmethod
    def from_orekit(cls, time: Time, dop):
        """Convert from Orekit."""
        n_sats = dop.getGnssNb()
        gdop = dop.getGdop()
        hdop = dop.getHdop()
        pdop = dop.getPdop()
        tdop = dop.getTdop()
        vdop = dop.getVdop()
        return cls(time=time, n_sats=n_sats, gdop=gdop, hdop=hdop, pdop=pdop, tdop=tdop, vdop=vdop)


class DepthOfCoverage(BaseModel):
    """The `DepthOfCoverage` class.

    This class models the depth of coverage for an observer in a specific time frame.
    """

    min_sats: int = Field(description="Minimum number of visible satellites.")
    max_sats: int = Field(description="Maximum number of visible satellites.")


class NavigationResults(BaseModel):
    """The results of the `Navigation` analysis."""

    dop: dict[UUID4, list[DilutionOfPrecision]]

    @computed_field
    @property
    def depth_of_coverage(self) -> dict[UUID4, DepthOfCoverage]:
        return {
            asset_id: DepthOfCoverage(min_sats=min(d.n_sats for d in dop), max_sats=max(d.n_sats for d in dop))
            for asset_id, dop in self.dop.items()
        }

    def plot(self, observer: UUID4):
        """Plot the dilution of precision for a given observer."""
        dop = self.dop[observer]
        dts = [d.time.datetime for d in dop]
        n_sats = [d.n_sats for d in dop]
        gdop = [d.gdop for d in dop]
        hdop = [d.hdop for d in dop]
        pdop = [d.pdop for d in dop]
        tdop = [d.tdop for d in dop]
        vdop = [d.vdop for d in dop]

        fig, ax = plt.subplots(1, 2, figsize=(12, 8))
        plt.subplots_adjust(hspace=0.5)

        fig.suptitle(f"Navigation Performance from {dop[0].time.datetime.date()} to {dop[-1].time.datetime.date()}")

        for a in ax.flat:
            a.xaxis.set_major_locator(mdates.AutoDateLocator())
            a.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            a.xaxis.set_tick_params(rotation=45)
            a.grid()

        ax[0].plot(dts, n_sats)
        ax[0].set_title("Number of Visible Satellites")
        ax[1].plot(dts, gdop, label="GDOP")
        ax[1].plot(dts, hdop, label="HDOP")
        ax[1].plot(dts, pdop, label="PDOP")
        ax[1].plot(dts, tdop, label="TDOP")
        ax[1].plot(dts, vdop, label="VDOP")
        ax[1].set_title("Dilution of Precision")
        ax[1].legend(loc="upper right")


class Navigation(Analysis[NavigationResults]):
    """The `Navigation` analysis.

    This class analyses the dilution of precision and depth of coverage of a GNSS constellation for all observers in a
    given scenario.
    """

    scenario: Scenario
    start_time: Time | None = Field(default=None)
    end_time: Time | None = Field(default=None)

    def analyze(self, *, ensemble: Ensemble | None = None) -> NavigationResults:  # type: ignore
        """Run the analysis."""
        if not ensemble:
            ensemble = self.scenario.propagate()

        start_time = self.start_time or self.scenario.start_time
        end_time = self.end_time or self.scenario.end_time

        times = start_time.trange(end_time, self.scenario.time_step)

        sc = {
            sc_id: tra
            for sc_id, tra in ensemble.trajectories.items()
            if isinstance(self.scenario[sc_id].model, Spacecraft)
        }
        observers = {
            asset.asset_id: asset.model for asset in self.scenario.assets if isinstance(asset.model, GroundStation)
        }

        from java.util import ArrayList  # type: ignore

        ephemerides = ArrayList([trajectory_to_ephemeris(t) for t in sc.values()])

        dop = {}

        from org.orekit.bodies import (  # type: ignore
            CelestialBodyFactory,
            GeodeticPoint,
            OneAxisEllipsoid,
        )
        from org.orekit.gnss import DOPComputer  # type: ignore

        for obs_id, observer in observers.items():
            r_e = observer.body.equatorial_radius
            f = observer.body.flattening
            frame = CelestialBodyFactory.getBody(observer.body.name).getBodyOrientedFrame()
            shape = OneAxisEllipsoid(r_e, f, frame)
            point = GeodeticPoint(observer.latitude.radians, observer.longitude.radians, observer.altitude)
            computer = DOPComputer.create(shape, point)
            dop[obs_id] = [
                DilutionOfPrecision.from_orekit(t, computer.compute(time_to_abs_date(t), ephemerides))  # type: ignore
                for t in times
            ]

        return NavigationResults(dop=dop)
