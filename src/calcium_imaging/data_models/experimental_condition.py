from typing import List

import pandas as pd

from .coverslip import Coverslip


class ExperimentalCondition:
    """One experimental condition, e.g. 'shNCLX'."""

    def __init__(self, condition_type: str, coverslips_list: List[Coverslip]) -> None:
        """Holds multiple runs of the same experimental condition"""
        self.type = condition_type
        self.coverslips_list = sorted(coverslips_list, key=lambda coverslip: coverslip.id)
        if not all(cs.experimental_condition_type == condition_type for cs in self.coverslips_list):
            raise RuntimeError(
                f"Found coverslip with non suitable experimental condition for '{self.type}'")  # TODO more indicative
        self.df = pd.concat([coverslip.df for coverslip in self.coverslips_list], axis=1)
        self.cells_count = len(self.df.columns)

    def __repr__(self) -> str:
        return str(self.type)
