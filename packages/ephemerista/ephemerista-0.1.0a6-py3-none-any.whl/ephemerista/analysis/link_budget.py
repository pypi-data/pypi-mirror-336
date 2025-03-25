"""The link_budget.py module.

This module provides the `LinkBudget` class and the associated `LinkBudgetResults` class.
"""

from functools import partial
from typing import Literal, Self

import itur
import lox_space as lox
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itur.models import itu618, itu836
from pydantic import UUID4, Field, computed_field

from ephemerista import BaseModel
from ephemerista.analysis import Analysis
from ephemerista.analysis.visibility import Pass, Visibility, VisibilityResults, Window
from ephemerista.angles import Angle
from ephemerista.assets import Asset, AssetKey, GroundStation, Spacecraft, _asset_id
from ephemerista.comms.antennas import ParabolicPattern
from ephemerista.comms.channels import Channel
from ephemerista.comms.systems import CommunicationSystem
from ephemerista.comms.utils import free_space_path_loss, to_db
from ephemerista.ipy_widgets import with_plot_display_widget
from ephemerista.math import angle_between
from ephemerista.scenarios import Ensemble, Scenario
from ephemerista.time import Time, TimeDelta


class InterferenceStats(BaseModel):
    """The `InterferenceStats` class.

    This class models the influence of interfering radio transmissions on the link.
    """

    interference_power_w: float = Field(ge=0.0, description="Total received interference power from all sources, in W")
    c_n0i0: float = Field(description="Carrier to noise plus interference density, in dB")
    eb_n0i0: float = Field(description="Bit energy to noise plus interference density, in dB")
    margin_with_interference: float = Field(description="Link margin considering interference, in dB")

    @computed_field(description="Total received interference power in dBW")
    @property
    def interference_power(self) -> float:
        return to_db(self.interference_power_w) if self.interference_power_w > 0 else np.nan


def _off_boresight_angle(
    time: Time, ensemble: Ensemble, self: Asset, other: Asset, comms: CommunicationSystem
) -> float:
    self_state = ensemble[self].interpolate(time)
    other_state = ensemble[other].interpolate(time)
    if not self.tracked_object_id:
        # This asset does not track any object, using its antenna's boresight vector
        r = other_state.position - self_state.position
        ru = r / np.linalg.norm(r)
        if isinstance(self.model, Spacecraft):
            rot_eci_from_lvlh = self_state.rotation_lvlh()
            angle = angle_between(ru, rot_eci_from_lvlh @ comms.antenna.boresight_array)
        elif isinstance(self.model, GroundStation):
            rot_topocentric_from_eci = self.model._location.rotation_to_topocentric()
            angle = angle_between(ru, rot_topocentric_from_eci.T @ comms.antenna.boresight_array)
        else:
            # Default: towards zenith
            zenith = self_state.position
            angle = angle_between(r, zenith)

    elif self.tracked_object_id == other.asset_id:
        # This asset tracks the other asset under consideration, so zero angle
        angle = 0.0
    else:
        # This asset tracks a third asset, compute angle <other asset, this object, tracked asset>
        tracked_obj_state = ensemble[self.tracked_object_id].interpolate(time)
        this_to_other_obj = other_state.position - self_state.position
        this_to_tracked_obj = tracked_obj_state.position - self_state.position
        angle = angle_between(this_to_other_obj, this_to_tracked_obj)

    return max(0, angle)


class EnvironmentalLosses(BaseModel):
    """The `EnvironmentalLosses` class.

    This class models all environmental losses supported by Ephemerista.
    """

    rain_attenuation: float = Field(ge=0.0, description="Rain attenuation, in dB)")
    gaseous_attenuation: float = Field(ge=0.0, description="Gaseous attenuation, in dB")
    scintillation_attenuation: float = Field(ge=0.0, description="Solar scintillation attenuation, in dB")
    atmospheric_attenuation: float = Field(ge=0.0, description="Attenuation of atmospheric gases, in dB")
    cloud_attenuation: float = Field(ge=0.0, description="Attenuation due to clouds, in dB")
    depolarization_loss: float = Field(ge=0.0, description="Depolarization losses, in dB")

    def sum(self) -> float:
        """Sum all environmental losses."""
        return (
            self.rain_attenuation
            + self.gaseous_attenuation
            + self.scintillation_attenuation
            + self.atmospheric_attenuation
            + self.cloud_attenuation
            + self.depolarization_loss
        )

    @classmethod
    def no_losses(cls) -> Self:
        """Initialise losses to zero."""
        return cls(
            rain_attenuation=0,
            gaseous_attenuation=0,
            scintillation_attenuation=0,
            atmospheric_attenuation=0,
            cloud_attenuation=0,
            depolarization_loss=0,
        )

    @classmethod
    def calculate(
        cls,
        percentage_exceed: float,
        time: Time,
        observer: Asset,
        target_comms: CommunicationSystem,
        observer_comms: CommunicationSystem,
        gs_pass: Pass,
    ) -> Self:
        """Calculate environmental losses for a given link."""
        f = target_comms.transmitter.frequency
        f_ghz = f * 1e-9
        gs_lat_deg = observer.model.latitude.degrees
        gs_lon_deg = observer.model.longitude.degrees
        gs_alt_km = observer.model.altitude * 1e-3

        gs_ant_parabolic_equivalent = ParabolicPattern.from_beamwidth(observer_comms.antenna.beamwidth(f), f)
        gs_ant_dia = gs_ant_parabolic_equivalent.diameter
        gs_ant_eff = gs_ant_parabolic_equivalent.efficiency

        pass_observables = gs_pass.interpolate(time)
        el_deg = pass_observables.elevation.degrees

        # Computing rain attenuation
        rain_attenuation = itur.rain_attenuation(
            gs_lat_deg, gs_lon_deg, f_ghz, el_deg, gs_alt_km, percentage_exceed
        ).value

        # Computing depolarization loss
        depolarization_loss = 0
        if f_ghz > 4 and f_ghz <= 55:  # noqa: PLR2004
            xpd = itu618.rain_cross_polarization_discrimination(
                rain_attenuation,
                f_ghz,
                el_deg if el_deg < 60 else 60,  # noqa: PLR2004
                percentage_exceed,
            ).value
            depolarization_loss = to_db(1 + 1 / xpd)

        # Computing scintillation
        scintillation_attenuation = itur.scintillation_attenuation(
            gs_lat_deg, gs_lon_deg, f_ghz, el_deg, percentage_exceed, gs_ant_dia, gs_ant_eff
        ).value

        # Computing gaseous attenuation
        T = itur.surface_mean_temperature(gs_lat_deg, gs_lon_deg).value  # noqa: N806
        P = itur.standard_pressure(gs_lat_deg, gs_alt_km).value  # noqa: N806
        rho = itu836.surface_water_vapour_density(gs_lat_deg, gs_lon_deg, percentage_exceed, gs_alt_km).value
        gaseous_attenuation = itur.gaseous_attenuation_slant_path(f_ghz, el_deg, rho, P, T, h=gs_alt_km).value

        # Computing atmospheric attenuation
        atmospheric_attenuation = itur.atmospheric_attenuation_slant_path(
            gs_lat_deg, gs_lon_deg, f_ghz, el_deg, percentage_exceed, gs_ant_dia
        ).value

        # Computing cloud attenuation
        cloud_attenuation = itur.cloud_attenuation(gs_lat_deg, gs_lon_deg, el_deg, f_ghz, percentage_exceed).value

        return cls(
            rain_attenuation=rain_attenuation,
            gaseous_attenuation=gaseous_attenuation,
            scintillation_attenuation=scintillation_attenuation,
            atmospheric_attenuation=atmospheric_attenuation,
            cloud_attenuation=cloud_attenuation,
            depolarization_loss=depolarization_loss,
        )


class LinkStats(BaseModel):
    """The `LinkStats` class.

    This class models all relevant properties of a radio link for link budget calculations at specific point in time.
    """

    slant_range: float = Field(description="Range between transmit and receive antennas, in meters")
    fspl: float = Field(description="Free space path loss, in dB")
    tx_angle: Angle = Field(
        description="Angle between the TX antenna boresight vector and the transmitter to receiver vector, in degrees"
    )
    rx_angle: Angle = Field(
        description="Angle between the RX antenna boresight vector and the receiver to transmitter vector, in degrees"
    )
    eirp: float = Field(description="Effective isotropic radiated power, in dBW")
    gt: float = Field(description="Gain to noise temperature ratio, in dB/K")
    c_n0: float = Field(description="Carrier to noise density, in dB")
    eb_n0: float = Field(description="Bit energy to noise density, in dB")
    margin: float = Field(description="Link margin, in dB")
    losses: EnvironmentalLosses = Field(description="Environmental losses")
    carrier_rx_power: float = Field(description="Power level at receiver input, in dBW")
    data_rate: float = Field(description="Data rate, in bit/s")
    bandwidth: float = Field(description="Bandwidth, in Hz")
    frequency: float = Field(description="Frequency, in Hz")
    noise_power: float = Field(description="Noise power, in dBW")
    interference_stats: InterferenceStats | None = Field(
        default=None, description="Interference data (optional, only available after analyzing interference)"
    )

    @classmethod
    def calculate(
        cls,
        time: Time,
        channel: Channel,
        link_type: Literal["uplink", "downlink"],
        target: Asset,
        observer: Asset,
        target_comms: CommunicationSystem,
        observer_comms: CommunicationSystem,
        losses: EnvironmentalLosses,
        ensemble: Ensemble,
    ) -> Self:
        """Calculate link stats."""
        sc_state = ensemble[target].interpolate(time)
        gs_state = ensemble[observer].interpolate(time)

        sc_angle = _off_boresight_angle(time, ensemble, target, observer, target_comms)
        gs_angle = _off_boresight_angle(time, ensemble, observer, target, observer_comms)

        slant_range = float(np.linalg.norm(sc_state.position - gs_state.position))
        if link_type == "uplink":
            rx_angle = sc_angle
            tx_angle = gs_angle
            rx = target_comms
            tx = observer_comms
        else:
            rx_angle = gs_angle
            tx_angle = sc_angle
            rx = observer_comms
            tx = target_comms
        if not tx.transmitter:
            msg = "Transmitter not found"
            raise ValueError(msg)
        if not rx.receiver:
            msg = "Receiver not found"
            raise ValueError(msg)
        frequency = tx.transmitter.frequency
        bandwidth = channel.bandwidth
        fspl = free_space_path_loss(slant_range, frequency)
        eirp = tx.transmitter.equivalent_isotropic_radiated_power(tx.antenna, tx_angle)
        gt = rx.receiver.gain_to_noise_temperature(rx.antenna, rx_angle)
        carrier_rx_power = tx.carrier_power(rx, losses.sum(), slant_range, tx_angle, rx_angle)
        noise_power = tx.noise_power(rx, bandwidth)
        c_n0 = tx.carrier_to_noise_density(rx, losses.sum(), slant_range, tx_angle, rx_angle)
        eb_n0 = channel.bit_energy_to_noise_density(tx, rx, losses.sum(), slant_range, tx_angle, rx_angle)
        margin = eb_n0 - channel.required_eb_n0 - channel.margin
        return cls(
            slant_range=slant_range,
            fspl=fspl,
            tx_angle=Angle.from_radians(tx_angle),
            rx_angle=Angle.from_radians(rx_angle),
            eirp=eirp,
            gt=gt,
            c_n0=c_n0,
            eb_n0=eb_n0,
            margin=margin,
            losses=losses,
            carrier_rx_power=carrier_rx_power,
            data_rate=channel.data_rate,
            bandwidth=bandwidth,
            frequency=frequency,
            noise_power=noise_power,
        )

    def add_interference(self, interference_power_w: float) -> Self:
        """Add interference to previously computed link stats."""
        c_n0i0 = CommunicationSystem._recompute_c_n0i0(
            self.carrier_rx_power, self.noise_power, self.bandwidth, interference_power_w
        )
        eb_n0i0 = Channel._recompute_eb_n0i0(
            self.carrier_rx_power, self.noise_power, self.bandwidth, interference_power_w, self.data_rate
        )
        margin_with_interference = self.margin + eb_n0i0 - self.eb_n0

        return self.model_copy(
            update={
                "interference_stats": InterferenceStats(
                    interference_power_w=interference_power_w,
                    c_n0i0=c_n0i0,
                    eb_n0i0=eb_n0i0,
                    margin_with_interference=margin_with_interference,
                )
            }
        )


class Link(BaseModel):
    """The `Link` class.

    This class models a radio link between two communication systems covering a specific visbility window.
    """

    window: Window = Field(description="Time window of the visibility pass where the link budget is computed")
    link_type: Literal["uplink", "downlink"] = Field(description="Link type, uplink or downlink")
    times: list[Time] = Field(description="Time vector")
    stats: list[LinkStats] = Field(description="List of link metrics, one for each time step")

    def to_dataframe(self) -> pd.DataFrame:
        """Convert to a `DataFrame`."""
        data = []
        for s in self.stats:
            link_dict = s.model_dump(exclude={"interference_stats", "losses"})
            link_dict.update(s.losses.model_dump())
            link_dict["losses_sum"] = s.losses.sum()
            if s.interference_stats:
                link_dict.update(s.interference_stats.model_dump())
            else:
                # No interference data, just writing no interference power and same link metrics
                link_dict.update(
                    InterferenceStats(
                        interference_power_w=0.0, c_n0i0=s.c_n0, eb_n0i0=s.eb_n0, margin_with_interference=s.margin
                    )
                )
            data.append(link_dict)

        df = pd.DataFrame.from_records(data, index=[t.datetime for t in self.times])
        return df

    def plot(self, *, plot_interference: bool = False):
        """Plot all link properties."""
        df = self.to_dataframe()

        fig, ax = plt.subplots(3, 3, figsize=(12, 8))
        plt.subplots_adjust(hspace=0.4, wspace=0.4)

        plot_title = f"{self.link_type.title()} from {self.window.start.to_utc()} to {self.window.stop.to_utc()}"
        if plot_interference:
            plot_title += ", with interference"
        fig.suptitle(plot_title)

        for a in ax.flat:
            a.xaxis.set_major_locator(mdates.HourLocator())
            a.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            a.xaxis.set_tick_params(rotation=45)
            a.grid()

        ax[0, 0].plot(df.index, df["slant_range"])
        ax[0, 0].set_title("Slant Range")
        ax[0, 0].set_ylabel("km")

        ax[0, 1].plot(df.index, df["tx_angle"], label="TX")
        ax[0, 1].plot(df.index, df["rx_angle"], label="RX")
        ax[0, 1].legend()
        ax[0, 1].set_title("Off Boresight Angles")
        ax[0, 1].set_ylabel("degrees")

        ax[0, 2].plot(df.index, df["fspl"])
        ax[0, 2].set_title("Free Space Path Loss")
        ax[0, 2].set_ylabel("dB")

        ax[1, 0].plot(df.index, df["eirp"])
        ax[1, 0].set_title("EIRP")
        ax[1, 0].set_ylabel("dBW")

        ax[1, 1].plot(df.index, df["gt"])
        ax[1, 1].set_title("G/T")
        ax[1, 1].set_ylabel("dB/K")

        ax[1, 2].plot(df.index, df["losses_sum"])
        ax[1, 2].set_title("Environment attenuations")
        ax[1, 2].set_ylabel("dB")

        ax[2, 0].plot(df.index, df["c_n0"], label="C/N0")
        if plot_interference:
            ax[2, 0].plot(df.index, df["c_n0i0"], label="C/(N0+I0)")
            ax[2, 0].legend()
        ax[2, 0].set_title("C/N0")
        ax[2, 0].set_ylabel("dB")

        ax[2, 1].plot(df.index, df["eb_n0"], label="Eb/N0")
        if plot_interference:
            ax[2, 1].plot(df.index, df["eb_n0i0"], label="Eb/(N0+I0)")
            ax[2, 1].legend()
        ax[2, 1].set_title("Eb/N0")
        ax[2, 1].set_ylabel("dB")

        ax[2, 2].plot(df.index, df["margin"], label="Margin")
        if plot_interference:
            ax[2, 2].plot(df.index, df["margin_with_interference"], label="Margin (with interference)")
            ax[2, 2].legend()
        ax[2, 2].set_title("Link Margin")
        ax[2, 2].set_ylabel("dB")

    def plot_attenuations(self, percentage_exceed: float):
        """Plot all attenuations."""
        df = self.to_dataframe()

        fig, ax = plt.subplots(2, 3, figsize=(10, 6))
        plt.subplots_adjust(hspace=0.4, wspace=0.4)

        plot_title = f"{self.window.start.to_utc()} to {self.window.stop.to_utc()}, attenuations exceeded {percentage_exceed}% of the time"  # noqa: E501
        fig.suptitle(plot_title)

        for a in ax.flat:
            a.xaxis.set_major_locator(mdates.HourLocator())
            a.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            a.xaxis.set_tick_params(rotation=45)
            a.grid()

        ax[0, 0].plot(df.index, df["rain_attenuation"])
        ax[0, 0].set_title("Rain attenuation")
        ax[0, 0].set_ylabel("dB")

        ax[0, 1].plot(df.index, df["gaseous_attenuation"])
        ax[0, 1].set_title("Gaseous attenuation")
        ax[0, 1].set_ylabel("dB")

        ax[0, 2].plot(df.index, df["scintillation_attenuation"])
        ax[0, 2].set_title("Scintillation attenuation")
        ax[0, 2].set_ylabel("dB")

        ax[1, 0].plot(df.index, df["atmospheric_attenuation"])
        ax[1, 0].set_title("Atmospheric attenuation")
        ax[1, 0].set_ylabel("dB")

        ax[1, 1].plot(df.index, df["cloud_attenuation"])
        ax[1, 1].set_title("Cloud attenuation")
        ax[1, 1].set_ylabel("dB")

        ax[1, 2].plot(df.index, df["depolarization_loss"])
        ax[1, 2].set_title("Depolarization loss")
        ax[1, 2].set_ylabel("dB")


@with_plot_display_widget
class LinkBudgetResults(BaseModel):
    """The results of the `LinkBudget` analysis."""

    links: dict[UUID4, dict[UUID4, list[Link]]] = Field(
        description="Dictionary of all links between all targets and all observers"
    )
    scenario: Scenario

    # Used by the ipywidget to be able to support flexible plotting
    _widget_data_field: str = "links"

    def get(self, observer: AssetKey, target: AssetKey) -> list[Link]:
        """Get all links for a given observer and target pairing."""
        target_passes = self.links.get(_asset_id(target), {})
        return target_passes.get(_asset_id(observer), [])

    def __getitem__(self, key: tuple[AssetKey, AssetKey]) -> list[Link]:
        """Get all links for a given observer and target pairing."""
        return self.get(*key)

    def to_dataframe(self, observer: AssetKey, target: AssetKey, *, with_interference: bool = False) -> pd.DataFrame:
        """Convert the analysis results to a Pandas data frame."""
        links = self.get(observer, target)
        data = []
        for link in links:
            slant_range = np.mean([s.slant_range for s in link.stats])
            tx_angle = np.mean([s.tx_angle.degrees for s in link.stats])
            rx_angle = np.mean([s.rx_angle.degrees for s in link.stats])
            fspl = np.mean([s.fspl for s in link.stats])
            eirp = np.mean([s.eirp for s in link.stats])
            gt = np.mean([s.gt for s in link.stats])
            losses = np.mean([s.losses.sum() for s in link.stats])
            c_n0 = np.mean([s.c_n0 for s in link.stats])
            eb_n0 = np.mean([s.eb_n0 for s in link.stats])
            margin = np.mean([s.margin for s in link.stats])

            row = {
                "start": link.window.start.datetime,
                "end": link.window.stop.datetime,
                "duration": link.window.duration,
                "type": link.link_type,
                "mean_slant_range": slant_range,
                "mean_tx_angle": tx_angle,
                "mean_rx_angle": rx_angle,
                "mean_fspl": fspl,
                "mean_eirp": eirp,
                "mean_gt": gt,
                "mean_losses": losses,
                "mean_c_n0": c_n0,
                "mean_eb_n0": eb_n0,
                "mean_margin": margin,
            }

            if with_interference:
                interference_power = []
                c_n0i0 = []
                eb_n0i0 = []
                margin_with_interference = []
                for s in link.stats:
                    s_interf = s.interference_stats
                    if s_interf:
                        interference_power.append(s_interf.interference_power)
                        c_n0i0.append(s_interf.c_n0i0)
                        eb_n0i0.append(s_interf.eb_n0i0)
                        margin_with_interference.append(s_interf.margin_with_interference)
                    else:
                        # No interference detected, so c_n0i0 = c_n0 and eb_n0i0 = eb_n0
                        interference_power.append(np.nan)
                        c_n0i0.append(s.c_n0)
                        eb_n0i0.append(s.eb_n0)
                        margin_with_interference.append(s.margin)

                row["mean_c_n0i0"] = np.mean(c_n0i0)
                row["mean_eb_n0i0"] = np.mean(eb_n0i0)
                row["mean_margin_interference"] = np.mean(margin_with_interference)

            data.append(row)
        return pd.DataFrame(data)


class LinkBudget(Analysis[LinkBudgetResults]):
    """The `LinkBudget` analysis."""

    scenario: Scenario = Field(description="The scenario used to analyze the link budget")
    start_time: Time | None = Field(
        default=None, description="Start time (optional, if None the scenario's start time is used)"
    )
    end_time: Time | None = Field(
        default=None, description="End time (optional, if None the scenario's end time is used)"
    )
    percentage_exceed: float = Field(
        gt=0.001,
        le=5.0,
        default=1.0,
        description="Percentage of the time the environmental attenuation values are exceeded, per ITU-R",
    )

    def analyze(
        self,
        ensemble: Ensemble | None = None,
        visibility: VisibilityResults | None = None,
        environment_losses: Literal["enabled", "disabled"] = "enabled",
    ) -> LinkBudgetResults:
        """Run the analysis."""
        if not ensemble:
            ensemble = self.scenario.propagate()

        if not visibility:
            visibility = Visibility(scenario=self.scenario, start_time=self.start_time, end_time=self.end_time).analyze(
                ensemble
            )

        # start_time = self.start_time or self.scenario.start_date
        # end_time = self.end_time or self.scenario.end_date

        links = {}

        for target_id, observers in visibility.passes.items():
            target = self.scenario[target_id]
            if not isinstance(target.model, Spacecraft):
                continue
            target_channels = set()
            for c in target.comms:
                target_channels.update(c.channels)

            if target_id not in links:
                links[target_id] = {}

            for observer_id, passes in observers.items():
                links[target_id][observer_id] = []

                observer = self.scenario[observer_id]
                if not isinstance(observer.model, GroundStation):
                    continue
                observer_channels = set()
                for c in observer.comms:
                    observer_channels.update(c.channels)

                channels = target_channels.intersection(observer_channels)
                if not channels:
                    continue

                for channel_id in channels:
                    channel = self.scenario.channel_by_id(channel_id)
                    link_type = channel.link_type
                    target_comms = target.comms_by_channel_id(channel_id)
                    observer_comms = observer.comms_by_channel_id(channel_id)

                    if link_type == "uplink":
                        rx = target_comms
                        tx = observer_comms
                    else:
                        rx = observer_comms
                        tx = target_comms

                    if not rx.receiver or not tx.transmitter:
                        continue

                    for gs_pass in passes:
                        t0 = gs_pass.window.start
                        t1 = gs_pass.window.stop
                        times = [float(t - t0) for t in gs_pass.times]
                        func = partial(
                            lambda t,
                            gs_pass,
                            channel,
                            link_type,
                            target,
                            observer,
                            target_comms,
                            observer_comms,
                            ensemble,
                            losses: _viability(
                                t,
                                gs_pass=gs_pass,
                                channel=channel,
                                link_type=link_type,
                                target=target,
                                observer=observer,
                                target_comms=target_comms,
                                observer_comms=observer_comms,
                                losses=losses,
                                ensemble=ensemble,
                            ),
                            gs_pass=gs_pass,
                            channel=channel,
                            link_type=link_type,
                            target=target,
                            observer=observer,
                            target_comms=target_comms,
                            observer_comms=observer_comms,
                            losses=EnvironmentalLosses.no_losses(),
                            ensemble=ensemble,
                        )

                        windows = lox.find_windows(
                            func,
                            t0._time,
                            t1._time,
                            times,
                        )

                        for w in windows:
                            window = Window._from_lox(w)
                            times = window.start.trange(window.stop, self.scenario.time_step)
                            stats = [
                                LinkStats.calculate(
                                    t,
                                    channel,
                                    link_type,
                                    target,
                                    observer,
                                    target_comms,
                                    observer_comms,
                                    EnvironmentalLosses.calculate(
                                        self.percentage_exceed,
                                        t,
                                        observer,
                                        target_comms,
                                        observer_comms,
                                        gs_pass,
                                    )
                                    if environment_losses == "enabled"
                                    else EnvironmentalLosses.no_losses(),
                                    ensemble,
                                )
                                for i, t in enumerate(times)
                            ]
                            links[target_id][observer_id].append(
                                Link(window=window, link_type=link_type, stats=stats, times=times)
                            )

        return LinkBudgetResults(links=links, scenario=self.scenario)


def _viability(
    t: float,
    *,
    gs_pass: Pass,
    channel: Channel,
    link_type: Literal["uplink", "downlink"],
    target: Asset,
    observer: Asset,
    target_comms: CommunicationSystem,
    observer_comms: CommunicationSystem,
    losses: EnvironmentalLosses,
    ensemble: Ensemble,
) -> float:
    time = gs_pass.window.start + TimeDelta(t)
    sc_state = ensemble[target].interpolate(time)
    gs_state = ensemble[observer].interpolate(time)

    sc_angle = _off_boresight_angle(time, ensemble, target, observer, target_comms)
    gs_angle = _off_boresight_angle(time, ensemble, observer, target, observer_comms)

    slant_range = float(np.linalg.norm(sc_state.position - gs_state.position))
    if link_type == "uplink":
        rx_angle = sc_angle
        tx_angle = gs_angle
        rx = target_comms
        tx = observer_comms
    else:
        rx_angle = gs_angle
        tx_angle = sc_angle
        rx = observer_comms
        tx = target_comms
    if not tx.transmitter:
        msg = "Transmitter not found"
        raise ValueError(msg)
    if not rx.receiver:
        msg = "Receiver not found"
        raise ValueError(msg)
    val = (
        channel.bit_energy_to_noise_density(tx, rx, losses.sum(), slant_range, tx_angle, rx_angle)
        - channel.required_eb_n0
        - channel.margin
    )

    return val
