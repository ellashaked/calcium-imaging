from typing import List

import pandas as pd

from .constants import BACKGROUND_FLUORESCENCE_ROIS, TIME_COL


class Preprocessor:
    def __init__(
            self,
            first_n_points_to_discard: int = 5,
            smoothing_windows_size: int = 2,
            time_col_name: str = TIME_COL,
            background_fluorescence_cols_names: List[str] = BACKGROUND_FLUORESCENCE_ROIS,
            normalization_sampling_start_frame: int = 1,
            normalization_sampling_end_frame: int = 35,
            drop_time_col: bool = True,
            drop_background_fluorescence_cols: bool = True
    ) -> None:
        self.first_n_points_to_discard = first_n_points_to_discard
        self.smoothing_windows_size = smoothing_windows_size
        self.time_col_name = time_col_name
        self.background_fluorescence_cols_names = background_fluorescence_cols_names
        self.normalization_sampling_start_frame = normalization_sampling_start_frame
        self.normalization_sampling_end_frame = normalization_sampling_end_frame
        self.drop_time_col = drop_time_col
        self.drop_background_fluorescence_cols = drop_background_fluorescence_cols

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy(deep=True)
        df = self.discard_first_n_points(df, n=self.first_n_points_to_discard)
        df = self.smoothen(df, window_size=self.smoothing_windows_size)
        df = self.subtract_background_fluorescence(df, self.background_fluorescence_cols_names)
        if self.drop_time_col:
            df = df.drop(columns=[self.time_col_name])
        if self.drop_background_fluorescence_cols:
            df = df.drop(columns=self.background_fluorescence_cols_names)
        df = self.normalize(
            df,
            sampling_start_frame=self.normalization_sampling_start_frame,
            sampling_end_frame=self.normalization_sampling_end_frame
        )
        return df

    @staticmethod
    def discard_first_n_points(df: pd.DataFrame, n: int) -> pd.DataFrame:
        return df.iloc[n:]

    @staticmethod
    def smoothen(df: pd.DataFrame, window_size: int = 2) -> pd.DataFrame:
        """Assuming df includes only cell ROIs (no dead / fluorescence background) ROIs or time cols"""
        return df.rolling(
            window=window_size,
            min_periods=1,  # allow smaller windows at edges
            center=True
        ).mean()

    @staticmethod
    def subtract_background_fluorescence(df: pd.DataFrame, background_fluorescence_cols: List[str]) -> pd.DataFrame:
        averaged = df[background_fluorescence_cols].mean(axis=1)
        result_df = df.subtract(averaged, axis=0)
        return result_df

    @staticmethod
    def normalize(df: pd.DataFrame, sampling_start_frame: int = 1, sampling_end_frame: int = 35) -> pd.DataFrame:
        """Assuming df includes only cell ROIs (no dead / fluorescence background) ROIs or time cols"""
        f0 = df.iloc[sampling_start_frame:sampling_end_frame].mean(axis=0)
        result_df = df.div(f0, axis=1)
        return result_df
