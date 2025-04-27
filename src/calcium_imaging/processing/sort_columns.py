import re

from pandas import DataFrame

from calcium_imaging.constants import TIME_COL


def sort_columns(df: DataFrame) -> DataFrame:
    roi_cols = df.columns.tolist()
    roi_cols.remove(TIME_COL)
    sorted_cols = [TIME_COL] + sorted(roi_cols, key=lambda s: int(re.search(r'\d+', s).group()))
    result_df = df[sorted_cols]
    assert len(df.columns) == len(result_df.columns)
    return result_df
