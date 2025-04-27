from typing import List

from .group import Group


class Experiment:
    """A folder containing multiple Conditions, e.g., 'SI_SH_check'."""

    def __init__(self, name: str, groups_list: List[Group]) -> None:
        """Holds multiple groups of the same experiment."""
        self.name = name
        self.groups_list = groups_list
        self.group_to_df = {
            group.group_type: group.df for group in groups_list
        }
        self.group_types = list(self.group_to_df.keys())
        self.num_groups = len(self.group_types)
