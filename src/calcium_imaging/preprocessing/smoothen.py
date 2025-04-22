from pandas import DataFrame


def smoothen(df: DataFrame, window_size: int = 2) -> DataFrame:
    """Assuming df includes only cell ROIs (no dead / fluorescence background) ROIs or time cols"""
    return df.rolling(
        window=window_size,
        min_periods=1,  # allow smaller windows at edges
        center=True
    ).mean()
