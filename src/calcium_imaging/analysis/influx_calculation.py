from typing import Optional

import pandas as pd

from .peak_detection import detect_peak_index
from .linear_fit import linear_fit
from .regression_coefficients import RegressionCoefficients1D

INFLUX_END_INDEX_OFFSET_FROM_PEAK = 1
INFLUX_START_INDEX_MIN_OFFSET_FROM_END = 2
INFLUX_START_INDEX_MAX_OFFSET_FROM_END = 60


def calculate_influx_linear_coefficients(
        trace: pd.Series,
        start_idx: Optional[int] = None,
        end_idx: Optional[int] = None
) -> RegressionCoefficients1D:
    start_idx = start_idx if start_idx is not None else detect_influx_start_index(trace)
    end_idx = end_idx if end_idx is not None else detect_influx_end_index(trace)
    if end_idx <= start_idx:
        raise RuntimeError(f"error calculating influx for trace '{trace.name}', end_idx <= start_idx")
    linear_coefficients = linear_fit(trace, start_idx, end_idx)
    if linear_coefficients.slope <= 0:
        print(f"Warning: influx is non-positive for trace '{trace.name}'")
    return linear_coefficients


def detect_influx_start_index(trace: pd.Series, peak_idx: Optional[int] = None) -> int:
    peak_idx = peak_idx if peak_idx is not None else detect_peak_index(trace)
    end_idx = detect_influx_end_index(trace, peak_idx)
    start_idx = end_idx - INFLUX_START_INDEX_MIN_OFFSET_FROM_END
    while start_idx > end_idx - INFLUX_START_INDEX_MAX_OFFSET_FROM_END:
        if trace.iloc[start_idx] <= 1.0 + 0.2 * (trace.max() - 1):  # at or below 20% baseline fluorescence level
            return start_idx
        start_idx -= 1
    return start_idx  # end_idx - INFLUX_START_INDEX_MAX_OFFSET_FROM_PEAK


def detect_influx_end_index(trace: pd.Series, peak_idx: Optional[int] = None) -> int:
    peak_idx = peak_idx if peak_idx is not None else detect_peak_index(trace)
    return peak_idx - INFLUX_END_INDEX_OFFSET_FROM_PEAK
