from typing import Optional

import pandas as pd

from .peak_detection import detect_peak_index
from .linear_fit import linear_fit
from .regression_coefficients import RegressionCoefficients1D

EFLUX_START_INDEX_OFFSET_FROM_PEAK = 5
EFLUX_END_INDEX_MAX_OFFSET_FROM_START = 30
EFLUX_END_INDEX_MIN_OFFSET_FROM_START = 3


def calculate_eflux_linear_coefficients(
        trace: pd.Series,
        start_idx: Optional[int] = None,
        end_idx: Optional[int] = None
) -> RegressionCoefficients1D:
    start_idx = start_idx if start_idx is not None else detect_eflux_start_index(trace, )
    if end_idx <= start_idx:
        raise RuntimeError(f"error calculating eflux for trace '{trace.name}', end_idx <= start_idx")
    linear_coefficients = linear_fit(trace, start_idx, end_idx)
    if linear_coefficients.slope >= 0:
        print(f"Warning: eflux is non-negative for trace '{trace.name}'")
    return linear_coefficients


def detect_eflux_start_index(trace: pd.Series) -> int:
    return detect_peak_index(trace) + EFLUX_START_INDEX_OFFSET_FROM_PEAK


def detect_eflux_end_index(trace: pd.Series) -> int:
    start_idx = detect_eflux_start_index(trace)
    end_idx = min(
        start_idx + EFLUX_END_INDEX_MAX_OFFSET_FROM_START,
        trace.index.values.max()  # prevent out of bounds
    )
    while end_idx > start_idx + EFLUX_END_INDEX_MIN_OFFSET_FROM_START:
        if trace.loc[end_idx] >= 1.0:  # above baseline fluorescence level
            return end_idx
        end_idx -= 1
    return end_idx  # start_idx + EFLUX_END_INDEX_MIN_OFFSET_FROM_START
