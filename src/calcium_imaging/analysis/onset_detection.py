import pandas as pd
import numpy as np


def detect_onset_index(
        trace: pd.Series,
        minimal_onset_index: int,
        maximal_onset_index: int,
        baseline_start_index: int,
        baseline_end_index: int,
        z_threshold: float = 3.0
) -> int:
    """
    Detects onset in a transient response trace by analyzing delta fluctuations.

    Parameters:
    - trace: pd.Series, the transient response signal
    - start_bound: int, lower bound index for searching onset
    - end_bound: int, upper bound index for searching onset
    - z_threshold: float, threshold in std deviations above baseline delta for onset detection

    Returns:
    - int: Index where onset is detected, or -1 if not detected
    """
    # Compute baseline deltas
    baseline_window = trace[baseline_start_index:baseline_end_index]
    baseline_deltas = np.abs(np.diff(baseline_window))
    baseline_mean = baseline_deltas.mean()
    baseline_std = baseline_deltas.std()
    threshold = baseline_mean + z_threshold * baseline_std

    # Search for first delta above threshold
    for i in range(minimal_onset_index, min(maximal_onset_index, len(trace) - 1)):
        delta = abs(trace.iloc[i + 1] - trace.iloc[i])
        if delta > threshold:
            return i + 1

    return minimal_onset_index
