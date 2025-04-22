from typing import List

from .condition import Condition


class Experiment:
    """A folder containing multiple Conditions, e.g., 'SI_SH_check'."""

    def __init__(self, name: str, conditions_list: List[Condition]) -> None:
        """Holds multiple conditions of the same experiment."""
        self.name = name
        self.condition_to_df = {condition.condition_type: condition for condition in conditions_list}
        self.condition_types = list(self.condition_to_df.keys())
