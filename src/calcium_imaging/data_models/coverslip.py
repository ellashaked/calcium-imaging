from typing import Dict

import pandas as pd
from typing_extensions import Self

from calcium_imaging.analysis import calculate_eflux_rate
from calcium_imaging.processing import sort_columns, preprocess_df


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
        self.df = preprocess_df(self.df)
        self.is_preprocessed = True
        return self

    def calculate_eflux_rates(self) -> Dict[str, float]:
        if not self.is_preprocessed:
            raise RuntimeError(f"Cannot calculate eflux for an unprocessed coverslip. "
                               f"Please call cs.preprocess() before calculating eflux.")
        return {
            roi_name: calculate_eflux_rate(series)
            for roi_name, series in self.df.iteritems()
        }
