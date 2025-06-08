import pandas as pd

def detect_baseline_return_idx(trace: pd.Series, eflux_start_idx: int) -> int:
    """
    Detects the index where the trace crosses the eflux linear fit (returns to baseline).
    Args:
        trace (pd.Series): The fluorescence trace.
        eflux_start_idx (int): Start index for eflux.
    Returns:
        int: Index where trace crosses the eflux linear fit.
    """
    for idx in range(eflux_start_idx, trace.index[-1], 1):
        if trace.loc[idx] <= 1:
            return idx
    return trace.index[-1]