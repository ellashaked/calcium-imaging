import pandas as pd

from calcium_imaging.analysis import detect_peak, linear_fit


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

    def calculate_eflux(self) -> float:  # TODO magic numbers
        start_idx = detect_peak(self.series) + 5
        end_idx = start_idx + 15
        linear_coefficients = linear_fit(self.series, start_idx, end_idx)
        eflux = linear_coefficients.slope
        return eflux

    def __repr__(self) -> str:
        return self.name
