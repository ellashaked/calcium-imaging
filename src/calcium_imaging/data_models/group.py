from typing import List

import pandas as pd

from .coverslip import Coverslip


class Group:
    """One group with certain intervention, e.g. 'shNCLX'."""

    def __init__(self, coverslips: List[Coverslip]) -> None:
        """Holds multiple runs of the same group"""
        self.coverslips = self._init_coverslips(coverslips)
        self.group_type = self._infer_group_type()
        self.cells_count = len(coverslips)

    def get_df(self) -> pd.DataFrame:
        return pd.concat([cs.get_df() for cs in self.coverslips], axis=1)

    def __repr__(self) -> str:
        return str(self.group_type)

    @staticmethod
    def _init_coverslips(coverslips: List[Coverslip]) -> List[Coverslip]:
        coverslips = sorted(coverslips, key=lambda cs: cs.id)
        if len(coverslips) == 0:
            raise ValueError(f"Initializing class Group with empty Coverslips list is illegal.")
        if not all([cs.group_type == coverslips[0].group_type for cs in coverslips]):
            raise ValueError(f"All Coverslips must share the same group type.")
        return coverslips

    def _infer_group_type(self) -> str:
        return self.coverslips[0].group_type
