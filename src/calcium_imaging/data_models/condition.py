from typing import List

import pandas as pd

from .run import Run


class Condition:
    """One experimental condition, e.g. 'shNCLX'."""

    def __init__(self, condition_type: str, runs_list: List[Run]) -> None:
        """Holds multiple runs of the same condition"""
        self.condition_type = condition_type
        self.runs_list = sorted(runs_list, key=lambda run: run.id)
        if not all(run.condition_type == condition_type for run in self.runs_list):
            raise RuntimeError(
                f"Found run with non suitable condition for '{self.condition_type}'")  # TODO more indicative
        self.df = pd.concat([run.df for run in self.runs_list], axis=1)
        self.cells_count = len(self.df.columns)

    def __repr__(self) -> str:
        return str(self.condition_type)
