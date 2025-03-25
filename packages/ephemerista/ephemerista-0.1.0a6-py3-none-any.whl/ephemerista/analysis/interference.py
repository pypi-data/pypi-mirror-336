"""The interference.py module.

This module provides the `Interference` class for conducting interference analyses.
"""

import numpy as np
from pydantic import Field

from ephemerista.analysis import Analysis
from ephemerista.analysis.link_budget import Link, LinkBudget, LinkBudgetResults
from ephemerista.comms.utils import from_db
from ephemerista.scenarios import Ensemble, Scenario
from ephemerista.time import Time


class Interference(Analysis[LinkBudgetResults]):
    """Interference analysis."""

    scenario: Scenario | None = Field(
        default=None,
        description="""The scenario used to analyze the interference. Optional because the analysis can be carried out
on LinkBudgetResults instead""",
    )
    start_time: Time | None = Field(
        default=None, description="Start time (optional, if None the scenario's start time is used)"
    )
    end_time: Time | None = Field(
        default=None, description="End time (optional, if None the scenario's end time is used)"
    )

    def analyze_uplink_interference(self, link_budget_results: LinkBudgetResults) -> LinkBudgetResults:
        """Analyzes uplink interference."""
        for target_id, target_passes in link_budget_results.links.items():
            # Target=spacecraft

            for observer_id, links in target_passes.items():
                for i_link, link in enumerate(links):
                    if link.link_type != "uplink":
                        continue

                    if not link.stats:
                        continue

                    # Sum of received power from other sources (weighted by band overlap), in WATTS, not dB
                    rx_powers_from_other_sources_w = np.zeros(len(link.stats))

                    # Iterate other ground stations
                    for other_observer_id, other_links in target_passes.items():
                        if other_observer_id == observer_id:
                            continue

                        for other_link in other_links:
                            if other_link.link_type != "uplink":
                                continue

                            # Interpolate RX power from other source and applying frequency band overlap factor
                            interf_power_from_source = _get_interfering_power_w(link, other_link)
                            if interf_power_from_source is not None:
                                rx_powers_from_other_sources_w += interf_power_from_source

                        # Adding interference metrics to link stats
                        link_stats_with_interf = []
                        for link_stats, interference_power_w in zip(
                            link.stats, rx_powers_from_other_sources_w, strict=False
                        ):
                            link_stats_with_interf.append(link_stats.add_interference(interference_power_w))

                        link_budget_results.links[target_id][observer_id][i_link].stats = link_stats_with_interf

        return link_budget_results

    def analyze_downlink_interference(self, link_budget_results: LinkBudgetResults) -> LinkBudgetResults:
        """Analyze downlink interference."""
        for target_id, target_passes in link_budget_results.links.items():
            # Target=spacecraft
            for observer_id, links in target_passes.items():
                for i_link, link in enumerate(links):
                    if link.link_type != "downlink":
                        continue

                    if not link.stats:
                        continue

                    # Sum of received power from other sources (weighted by band overlap), in WATTS, not dB
                    rx_powers_from_other_sources_w = np.zeros(len(link.stats))

                    # Iterate other spacecraft
                    for other_target_id, other_target_passes in link_budget_results.links.items():
                        if other_target_id == target_id:
                            continue

                        for other_observer_id, other_links in other_target_passes.items():
                            # Select passes of other spacecraft over the same ground station
                            if observer_id != other_observer_id:
                                continue

                            for other_link in other_links:
                                if other_link.link_type != "downlink":
                                    continue

                                # Interpolate RX power from other source and applying frequency band overlap factor
                                interf_power_from_source = _get_interfering_power_w(link, other_link)
                                if interf_power_from_source is not None:
                                    rx_powers_from_other_sources_w += interf_power_from_source

                    # Adding interference metrics to link stats
                    link_stats_with_interf = []
                    for link_stats, interference_power_w in zip(
                        link.stats, rx_powers_from_other_sources_w, strict=False
                    ):
                        link_stats_with_interf.append(link_stats.add_interference(interference_power_w))

                    link_budget_results.links[target_id][observer_id][i_link].stats = link_stats_with_interf

        return link_budget_results

    def analyze(  # type: ignore
        self,
        ensemble: Ensemble | None = None,
        link_budget_results: LinkBudgetResults | None = None,
    ) -> LinkBudgetResults:
        """Run the interference analysis."""
        if not link_budget_results:
            if not self.scenario:
                msg = "At least one of scenario, ensemble or link_budget_results must be non-None"
                raise ValueError(msg)
            if not ensemble:
                ensemble = self.scenario.propagate()
            link_budget_results = LinkBudget(
                scenario=self.scenario, start_time=self.start_time, end_time=self.end_time
            ).analyze(ensemble)
        else:
            link_budget_results = link_budget_results.model_copy()

        link_budget_results = self.analyze_uplink_interference(link_budget_results)
        link_budget_results = self.analyze_downlink_interference(link_budget_results)

        return link_budget_results


def _get_interfering_power_w(ref_link: Link, interfering_link: Link) -> None | np.ndarray:
    if not ref_link.stats:
        return

    if not interfering_link.stats:
        return

    interfering_power_w = np.zeros(len(ref_link.stats))
    link_freq = ref_link.stats[0].frequency
    link_bw = ref_link.stats[0].bandwidth
    t0 = ref_link.times[0]
    # Converting time to relative (seconds) for interpolation
    times_rel = [(time - t0).to_decimal_seconds() for time in ref_link.times]

    # Find passes for this spacecraft and these two ground stations which overlap in time
    if not are_time_wins_overlapping(
        ref_link.window.start, ref_link.window.stop, interfering_link.window.start, interfering_link.window.stop
    ):
        return

    # Compute frequency band overlap
    other_link_freq = interfering_link.stats[0].frequency
    other_link_bw = interfering_link.stats[0].bandwidth
    overlap_factor = get_overlap_factor(link_freq, link_bw, other_link_freq, other_link_bw)
    if overlap_factor <= 0.0:
        return

    other_times_rel = [(time - t0).to_decimal_seconds() for time in interfering_link.times]
    # Add interfering contribution, weighted by frequency band overlap
    interfering_power_w = overlap_factor * np.interp(
        times_rel,
        other_times_rel,
        from_db(np.array([s.carrier_rx_power for s in interfering_link.stats])),
        left=0,
        right=0,
    )

    return interfering_power_w


def are_time_wins_overlapping(w1_start: Time, w1_end: Time, w2_start: Time, w2_end: Time) -> bool:
    """Check if two time windows are overlapping."""
    return ((w2_start - w1_end).to_decimal_seconds() <= 0) and ((w1_start - w2_end).to_decimal_seconds() <= 0)


def get_overlap_factor(center_freq_1: float, bw1: float, center_freq_2: float, bw2: float) -> float:
    """
    Return overlap factor between two frequency bands.

    The factor is between 0 and 1 and relative to the bandwidth of the first frequency band
    """
    fmax_1 = center_freq_1 + bw1 / 2
    fmin_1 = center_freq_1 - bw1 / 2
    fmax_2 = center_freq_2 + bw2 / 2
    fmin_2 = center_freq_2 - bw2 / 2

    overlapping_bw = min(fmax_1 - fmin_2, fmax_2 - fmin_1)
    if overlapping_bw < 0:
        # no overlap
        return 0.0

    return overlapping_bw / bw1
