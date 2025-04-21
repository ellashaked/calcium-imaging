from typing import List

from .run import Run


class Condition:
    """One experimental condition, e.g. 'shNCLX'."""

    def __init__(self, runs_list: List[Run]) -> None:
        """Holds multiple runs of the same condition"""
        self.runs_list = runs_list
        assert len(runs_list) > 0 and all(run.condition == self.runs_list[0].condition for run in self.runs_list)
