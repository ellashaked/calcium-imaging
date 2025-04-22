from typing import List

from pandas import DataFrame


def subtract_background_fluorescence(df: DataFrame, background_fluorescence_cols: List[str]) -> DataFrame:
    averaged = df[background_fluorescence_cols].mean(axis=1)
    result_df = df.subtract(averaged, axis=0)
    return result_df
