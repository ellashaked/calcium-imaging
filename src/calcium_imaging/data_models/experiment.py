from typing import List

from .experimental_condition import ExperimentalCondition


class Experiment:
    """A folder containing multiple Conditions, e.g., 'SI_SH_check'."""

    def __init__(self, name: str, experimental_conditions_list: List[ExperimentalCondition]) -> None:
        """Holds multiple experimental conditions of the same experiment."""
        self.name = name
        self.experimental_condition_to_df = {condition.type: condition for condition in experimental_conditions_list}
        self.experimental_condition_types = list(self.experimental_condition_to_df.keys())
