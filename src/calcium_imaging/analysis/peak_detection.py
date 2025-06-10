import pandas as pd
from .onset_detection import detect_onset_index


def detect_peak_index(
        trace: pd.Series,
        end_bound: int = 120,
        baseline_window: int = 30,
        sliding_window: int = 3,
        threshold_factor: float = 3.0
) -> int:
    """
    Detects a peak in a trace within the given bounds.

    Parameters:
    - trace: pd.Series of numeric values
    - start_bound: start index for peak search
    - end_bound: end index for peak search
    - baseline_window: window size before start_bound to estimate noise level
    - sliding_window: how many points to consider when comparing local max
    - threshold_factor: peak must exceed baseline by this factor (std units)

    Returns:
    - Index of detected peak (int)
    """
    start_bound = detect_onset_index(trace)

    baseline = trace.iloc[start_bound - baseline_window:start_bound]
    baseline_mean = baseline.mean()
    baseline_std = baseline.std()

    for i in range(start_bound + sliding_window, end_bound - sliding_window):
        current = trace.iloc[i]
        neighbors = trace.iloc[i - sliding_window:i + sliding_window + 1]
        if (current == neighbors.max() and
                current > baseline_mean + threshold_factor * baseline_std):
            return trace.index[i]

    # fallback
    return trace.index.values.iloc[start_bound:][trace.argmax()]
