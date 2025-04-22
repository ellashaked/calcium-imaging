from pandas import DataFrame


def normalize(df: DataFrame, sampling_start_frame: int = 1, sampling_end_frame: int = 35) -> DataFrame:
    """Assuming df includes only cell ROIs (no dead / fluorescence background) ROIs or time cols"""
    f0 = df.iloc[sampling_start_frame:sampling_end_frame].mean(axis=0)
    result_df = df.div(f0, axis=1)
    return result_df
