import pandas as pd


def detect_peak(series: pd.Series) -> int:
    return series.argmax()
