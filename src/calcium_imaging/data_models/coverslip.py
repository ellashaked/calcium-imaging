from typing import Dict

import pandas as pd

from calcium_imaging.analysis import calculate_eflux_rate


class Coverslip:
    """One plate"""

    def __init__(self, name: str, df: pd.DataFrame) -> None:
        """Reads an Excel path and turns it into a Coverslip object"""
        self.name = name
        self.raw_df = df
        self.df = self.raw_df.copy(deep=True)
        self.id = int(self.name.split("-")[0].strip())  # TODO regex
        self.group_type = self.name.split("-")[-1].strip()  # TODO regex

    def __repr__(self) -> str:
        return str(self.name)

    def calculate_eflux_rates(self) -> Dict[str, float]:
        return {
            roi_name: calculate_eflux_rate(series)
            for roi_name, series in self.df.iteritems()
        }
