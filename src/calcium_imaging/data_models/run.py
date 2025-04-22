from typing_extensions import Self

import pandas as pd

from calcium_imaging.constants import BACKGROUND_FLUORESCENCE_ROIS, TIME_COL
from calcium_imaging.preprocessing import (
    discard_first_n_points,
    subtract_background_fluorescence,
    smoothen,
    normalize,
    sort_columns
)


class Run:
    """One plate"""

    def __init__(self, name: str, df: pd.DataFrame) -> None:
        """Reads an Excel path and turns it into a run object"""
        self.name = name
        self.raw_df = sort_columns(df)
        self.df = df.copy(deep=True)
        self.id = self.name.split("-")[0].strip()  # TODO regex
        self.condition_type = self.name.split("-")[-1].strip().lower()  # TODO regex

    def __repr__(self) -> str:
        return str(self.name)

    def preprocess(self) -> Self:  # TODO configure
        self.df = discard_first_n_points(self.df, n=5)
        self.df = smoothen(self.df, window_size=2)
        self.df = subtract_background_fluorescence(self.df, BACKGROUND_FLUORESCENCE_ROIS)
        self.df = self.df.drop(columns=[TIME_COL] + BACKGROUND_FLUORESCENCE_ROIS)
        self.df = normalize(self.df, sampling_start_frame=1, sampling_end_frame=35)
        return self
