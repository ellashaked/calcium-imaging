from .eflux_calculation import calculate_eflux_linear_coefficients
import pandas as pd

def detect_baseline_return_idx(trace: pd.Series, eflux_start_idx: int, eflux_end_idx: int) -> int:
    """
    Detects the index where the trace crosses the eflux linear fit (returns to baseline).
    Args:
        trace (pd.Series): The fluorescence trace.
        eflux_start_idx (int): Start index for eflux.
        eflux_end_idx (int): End index for eflux.
    Returns:
        int: Index where trace crosses the eflux linear fit.
    """
    coeffs = calculate_eflux_linear_coefficients(trace, eflux_start_idx, eflux_end_idx)
    for idx in range(eflux_start_idx, eflux_end_idx + 1):
        fit_val = coeffs.intercept + coeffs.slope * idx
        if trace.loc[idx] <= fit_val:
            return idx
    return eflux_end_idx 