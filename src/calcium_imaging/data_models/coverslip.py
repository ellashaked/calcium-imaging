from typing import Dict

from typing_extensions import Self

import pandas as pd

from calcium_imaging.analysis import linear_fit, detect_peak
from calcium_imaging.constants import BACKGROUND_FLUORESCENCE_ROIS, TIME_COL
from calcium_imaging.preprocessing_utils import (
    discard_first_n_points,
    subtract_background_fluorescence,
    smoothen,
    normalize,
    sort_columns,
    rename_columns
)


class Coverslip:
    """One plate"""

    def __init__(self, name: str, df: pd.DataFrame) -> None:
        """Reads an Excel path and turns it into a Coverslip object"""
        self.name = name
        self.raw_df = sort_columns(df)
        self.df = self.raw_df.copy(deep=True)
        self.id = int(self.name.split("-")[0].strip())  # TODO regex
        self.group_type = self.name.split("-")[-1].strip()  # TODO regex
        self.is_preprocessed = False

    def __repr__(self) -> str:
        return str(self.name)

    def preprocess(self) -> Self:  # TODO configure
        self.df = discard_first_n_points(self.df, n=5)
        self.df = smoothen(self.df, window_size=2)
        self.df = subtract_background_fluorescence(self.df, BACKGROUND_FLUORESCENCE_ROIS)
        self.df = self.df.drop(columns=[TIME_COL] + BACKGROUND_FLUORESCENCE_ROIS)
        self.df = normalize(self.df, sampling_start_frame=1, sampling_end_frame=35)
        self.df = rename_columns(self.df, f"cs-{self.id}")
        self.is_preprocessed = True
        return self

    def calculate_eflux_rates(self) -> Dict[str, float]:
        if not self.is_preprocessed:
            raise RuntimeError(f"Cannot calculate eflux for an unprocessed coverslip. "
                               f"Please call cs.preprocess() before calculating eflux.")
        roi_to_eflux = dict()
        for roi_name, series in self.df.iteritems():
            start_idx = detect_peak(series)
            end_idx = start_idx + 5  # TODO magic number
            linear_coefficients = linear_fit(series, start_idx, end_idx)
            eflux = linear_coefficients.slope
            roi_to_eflux[str(roi_name)] = eflux
        return roi_to_eflux
