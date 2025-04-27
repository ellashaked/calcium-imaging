import pandas as pd

from calcium_imaging.analysis import detect_peak, linear_fit


class ROI:
    """Single region of interest"""

    def __init__(self, name: str, series: pd.Series) -> None:
        self.name = name
        self.series = series

    def calculate_eflux(self) -> float:  # TODO magic numbers
        start_idx = detect_peak(self.series) + 5
        end_idx = start_idx + 15
        linear_coefficients = linear_fit(self.series, start_idx, end_idx)
        eflux = linear_coefficients.slope
        return eflux
