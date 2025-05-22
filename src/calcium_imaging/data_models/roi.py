from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from calcium_imaging.analysis import linear_fit, RegressionCoefficients1D, detect_peak_index
from calcium_imaging.viz import create_traces_figure


class ROI:
    """Single region of interest TODO maybe rename to cell / response"""
    EFLUX_START_INDEX_OFFSET_FROM_PEAK = 5
    EFLUX_END_INDEX_MAX_OFFSET_FROM_START = 30
    EFLUX_END_INDEX_MIN_OFFSET_FROM_START = 3
    FLUORESCENCE_CORRUPTION_THRESHOLD = 0.8

    def __init__(
            self,
            coverslip_id: int,
            roi_id: int,
            trace: pd.Series
    ) -> None:
        self.coverslip_id = coverslip_id
        self.roi_id = roi_id
        self.name = f"cs-{self.coverslip_id}_roi-{self.roi_id}"
        self.trace = trace.copy(deep=True).rename(self.name)
        self._peak_idx = detect_peak_index(self.trace)

    def __repr__(self) -> str:
        return self.name

    def calculate_eflux(self) -> float:
        return self._calculate_eflux_linear_coefficients().slope

    def calculate_amplitude(self) -> float:
        return self.trace[self._peak_idx] - 1

    def set_peak_idx(self, peak_idx: int) -> None:
        """Manually set peak idx using user input"""
        self._peak_idx = peak_idx

    def visualize(self, title_prefix: Optional[str] = None) -> None:
        base_title = f"ROI {self.roi_id} (Coverslip {self.coverslip_id})"
        create_traces_figure(
            main_trace=self.trace,
            title=base_title if title_prefix is None else f"{title_prefix}\n{base_title}",
            xaxis_title="Frame",
            yaxis_title="Fluorescence relative to background",
            yaxis_range=(0.5, max(2.5, self.trace.max())),
            highlight_index=self._peak_idx,
            eflux_linear_coefficients=self._calculate_eflux_linear_coefficients()
        ).show()

    def _get_eflux_start_index(self) -> int:
        return self._peak_idx + self.EFLUX_START_INDEX_OFFSET_FROM_PEAK

    def _get_eflux_end_index(self) -> int:
        start_idx = self._get_eflux_start_index()
        end_idx = min(
            start_idx + self.EFLUX_END_INDEX_MAX_OFFSET_FROM_START,
            self.trace.index.values.max()  # prevent out of bounds
        )
        while end_idx > start_idx + self.EFLUX_END_INDEX_MIN_OFFSET_FROM_START:
            if self.trace.loc[end_idx] >= 1.0:  # above baseline fluorescence level
                return end_idx
            end_idx -= 1
        return end_idx  # start_idx + self.EFLUX_END_INDEX_MIN_OFFSET_FROM_START

    def _calculate_eflux_linear_coefficients(self) -> RegressionCoefficients1D:  # TODO magic numbers
        start_idx = self._get_eflux_start_index()
        end_idx = self._get_eflux_end_index()
        if end_idx <= start_idx:
            raise RuntimeError(f"error calculating eflux in {self.name}, end_idx <= start_idx")
        linear_coefficients = linear_fit(self.trace, start_idx, end_idx)
        return linear_coefficients

    def _plot_trace(self) -> None:
        plt.plot(self.trace)

    def _highlight_peak(self) -> None:
        x = self._peak_idx
        y = self.trace[x]
        plt.scatter(x, y, color='red', s=100)

    def _plot_eflux(self) -> None:
        linear_coefficients = self._calculate_eflux_linear_coefficients()
        x = self.trace.index.values
        y = linear_coefficients.intercept + linear_coefficients.slope * x
        plt.plot(x, y, linestyle='--', color='black', zorder=3)

    def _plot_corruption_warning(self) -> None:
        """Shows a danger sign in case we are under corruption threshold"""
        skip = 0
        for xi, yi in self.trace.items():
            # If we're still in a skip window, just decrement and move on
            if skip > 0:
                skip -= 1
            # Otherwise, check the threshold
            elif yi < self.FLUORESCENCE_CORRUPTION_THRESHOLD:
                # draw your warning sign
                plt.text(
                    xi, yi,
                    u'\u26A0',  # Unicode warning sign
                    fontsize=14,
                    ha='center',
                    va='bottom'
                )
                # now skip the next 5 iterations
                skip = 5
