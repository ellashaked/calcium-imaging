from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from calcium_imaging.analysis import linear_fit, RegressionCoefficients1D


class ROI:
    """Single region of interest"""
    EFLUX_START_INDEX_OFFSET_FROM_PEAK = 5
    EFLUX_END_INDEX_MAX_OFFSET_FROM_START = 30
    EFLUX_END_INDEX_MIN_OFFSET_FROM_START = 10
    FLUORESCENCE_CORRUPTION_THRESHOLD = 0.8

    def __init__(
            self,
            coverslip_id: int,
            roi_id: int,
            series: pd.Series
    ) -> None:
        self.coverslip_id = coverslip_id
        self.roi_id = roi_id
        self.name = f"cs-{self.coverslip_id}_roi-{self.roi_id}"
        self.series = series.copy(deep=True).rename(self.name)

    def _get_eflux_start_index(self) -> int:
        return self.get_peak_frame() + 5

    def _get_eflux_end_index(self) -> int:
        start_idx = self._get_eflux_start_index()
        end_idx = min(
            start_idx + self.EFLUX_END_INDEX_MAX_OFFSET_FROM_START,
            self.series.index.values.max()  # prevent out of bounds
        )
        while end_idx > start_idx + self.EFLUX_END_INDEX_MIN_OFFSET_FROM_START:
            if self.series.loc[end_idx] >= 1.0:  # above baseline fluorescence level
                return end_idx
            end_idx -= 1
        return end_idx  # start_idx + self.EFLUX_END_INDEX_MIN_OFFSET_FROM_START

    def _calculate_eflux_linear_coefficients(self) -> RegressionCoefficients1D:  # TODO magic numbers
        start_idx = self._get_eflux_start_index()
        end_idx = self._get_eflux_end_index()
        linear_coefficients = linear_fit(self.series, start_idx, end_idx)
        return linear_coefficients

    def calculate_eflux(self) -> float:
        return self._calculate_eflux_linear_coefficients().slope

    def get_peak_frame(self) -> int:
        return self.series.index.values[self.series.argmax()]

    def visualize(self, title_prefix: Optional[str] = None) -> None:
        title = self.name if title_prefix is None else f"{title_prefix}\n{self.name}"
        plt.title(title)
        plt.xlabel("Frame")
        plt.ylabel("Fluorescence relative to background")
        plt.ylim((0.5, max(2.5, self.series.max())))
        self._plot_series()
        self._highlight_peak()
        self._plot_eflux()
        self._plot_corruption_warning()
        plt.show()

    def _plot_series(self) -> None:
        plt.plot(self.series)

    def _highlight_peak(self) -> None:
        x = self.get_peak_frame()
        y = self.series[x]
        plt.scatter(x, y, color='red', s=100)

    def _plot_eflux(self) -> None:
        linear_coefficients = self._calculate_eflux_linear_coefficients()
        x = self.series.index.values
        y = linear_coefficients.intercept + linear_coefficients.slope * x
        plt.plot(x, y, linestyle='--', color='black', zorder=3)

    def _plot_corruption_warning(self) -> None:
        """Shows a danger sign in case we are under corruption threshold"""
        skip = 0
        for xi, yi in self.series.items():
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

    def __repr__(self) -> str:
        return self.name
