import pandas as pd

from calcium_imaging.analysis import detect_peak, linear_fit


def calculate_eflux_rate(series: pd.Series) -> float:
    start_idx = detect_peak(series) + 5  # todo magic numbers
    end_idx = start_idx + 15
    linear_coefficients = linear_fit(series, start_idx, end_idx)
    eflux = linear_coefficients.slope
    return eflux
