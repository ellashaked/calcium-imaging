import re

from pandas import DataFrame

pattern = re.compile(r'^ROI\s*(\d+)\s*\(Average\)$')


def _rename_col(s: str, prefix_: str) -> str:
    # replace s with "{prefix}_ROI-<number>"
    return pattern.sub(rf'{prefix_}_ROI-\1', s)


def rename_columns(df: DataFrame, prefix_: str) -> DataFrame:
    old_to_new_names = {col: _rename_col(col, prefix_).lower() for col in df.columns.tolist()}
    result_df = df.rename(columns=old_to_new_names)
    return result_df
