import pandas as pd


def detect_peak_index(trace: pd.Series) -> int:
    return trace.index.values[trace.argmax()]
