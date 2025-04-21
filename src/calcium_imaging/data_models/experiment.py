from typing import List

from .condition import Condition


class Experiment:
    """A folder containing multiple Conditions, e.g., 'SI_SH_check'."""

    def __init__(self, conditions_list: List[Condition]) -> None:
        """Holds multiple conditions of the same experiment."""
        self.conditions_list = conditions_list
