from pandas import DataFrame


def discard_first_n_points(df: DataFrame, n: int) -> DataFrame:
    return df.iloc[n:]
