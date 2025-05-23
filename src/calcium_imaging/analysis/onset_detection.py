import pandas as pd


def detect_onset_index(
        trace: pd.Series,
        start_bound: int = 40,
        end_bound: int = 80,
        baseline_window: int = 30,
        sliding_window: int = 3,
        threshold_factor: float = 3.0
) -> int:
    """
    Detects the onset of a transient in a trace within a given window.

    Parameters:
    - trace: pd.Series of numeric values
    - start_bound: index to start searching for the onset
    - end_bound: index to stop searching
    - baseline_window: number of points before start_bound to estimate baseline fluctuation
    - sliding_window: size of the moving average window (delta computed over this window)
    - threshold_factor: multiplier of baseline std to define onset

    Returns:
    - onset index (int) within bounds where signal "explodes"
    """
    if start_bound - baseline_window < 0:
        raise ValueError("Not enough data before start_bound to compute baseline")

    baseline = trace.iloc[start_bound - baseline_window:start_bound]
    baseline_std = baseline.diff().dropna().abs().mean()

    for i in range(start_bound, end_bound - sliding_window):
        window = trace.iloc[i:i + sliding_window]
        delta = window.diff().abs().mean()
        if delta > threshold_factor * baseline_std:
            return trace.index[i]

    print("No onset detected within the specified bounds")
    return start_bound
