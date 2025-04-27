from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from calcium_imaging.analysis import linear_fit, RegressionCoefficients1D


class ROI:
    """Single region of interest"""

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

    def _calculate_eflux_linear_coefficients(self) -> RegressionCoefficients1D:  # TODO magic numbers
        start_idx = self.get_peak_frame() + 5
        end_idx = start_idx + 30
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
        self._plot_series()
        self._highlight_peak()
        self._plot_eflux()
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

    def __repr__(self) -> str:
        return self.name
