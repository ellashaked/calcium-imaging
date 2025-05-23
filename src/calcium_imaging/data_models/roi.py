from typing import Optional

import pandas as pd

from calcium_imaging.analysis import (
    calculate_eflux_linear_coefficients,
    calculate_influx_linear_coefficients,
    detect_onset_index,
    detect_peak_index,
    detect_eflux_end_index,
)
from calcium_imaging.viz import create_traces_figure


class ROI:
    """Single region of interest"""
    EFLUX_START_INDEX_OFFSET_FROM_PEAK = 5

    def __init__(
            self,
            trace: pd.Series,
            roi_id: int,
            coverslip_id: int,
            group_type: str,
    ) -> None:
        self.coverslip_id = coverslip_id
        self.roi_id = roi_id
        self.group_type = group_type
        self.name = f"cs-{self.coverslip_id}_roi-{self.roi_id}"
        self.title = f"ROI {self.roi_id} (Coverslip {self.coverslip_id}, {self.group_type})"
        self.trace = trace.copy(deep=True).rename(self.name)
        self.onset_idx = detect_onset_index(self.trace)
        self.peak_idx = detect_peak_index(self.trace)
        self.influx_start_idx = self.onset_idx
        self.influx_end_idx = self.peak_idx
        self.eflux_start_idx = self.peak_idx + self.EFLUX_START_INDEX_OFFSET_FROM_PEAK
        self.eflux_end_idx = detect_eflux_end_index(self.trace)
        self.baseline_return_idx = None

    def calculate_influx(self) -> float:
        return calculate_influx_linear_coefficients(
            trace=self.trace,
            start_idx=self.influx_start_idx,
            end_idx=self.influx_end_idx
        ).slope

    def calculate_eflux(self) -> float:
        return calculate_eflux_linear_coefficients(
            trace=self.trace,
            start_idx=self.eflux_start_idx,
            end_idx=self.eflux_end_idx
        ).slope

    def calculate_amplitude(self) -> float:
        return self.trace[self.peak_idx] - 1

    def visualize(self, title_prefix: Optional[str] = None) -> None:
        influx_linear_coefficients = calculate_influx_linear_coefficients(
            trace=self.trace,
            start_idx=self.influx_start_idx,
            end_idx=self.influx_end_idx
        )
        eflux_linear_coefficients = calculate_eflux_linear_coefficients(
            trace=self.trace,
            start_idx=self.eflux_start_idx,
            end_idx=self.eflux_end_idx
        )
        create_traces_figure(
            main_trace=self.trace,
            title=self.title if title_prefix is None else f"{title_prefix}\n{self.title}",
            xaxis_title="Frame",
            yaxis_title="Fluorescence relative to background",
            main_trace_peak_index=self.peak_idx,
            main_trace_onset_index=self.onset_idx,
            eflux_linear_coefficients=eflux_linear_coefficients,
            influx_linear_coefficients=influx_linear_coefficients
        ).show()

    def __repr__(self) -> str:
        return self.name
