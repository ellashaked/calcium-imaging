import re

from pandas import DataFrame

pattern = re.compile(r'^ROI\s*(\d+)\s*\(Average\)$')


def _rename_col(s: str, prefix_: str) -> str:
    # replace s with "{prefix}_ROI-<number>"
    return pattern.sub(rf'{prefix_}_ROI-\1', s)


def rename_columns(df: DataFrame, prefix_: str) -> DataFrame:
    renamed_columns = [_rename_col(col, prefix_) for col in df.columns.tolist()]
    result_df = df[renamed_columns]
    return result_df
