from typing import List, Dict

import pandas as pd

from .group import Group


class Experiment:
    """A folder containing multiple Conditions, e.g., 'SI_SH_check'."""

    def __init__(self, name: str, groups: List[Group]) -> None:
        """Holds multiple groups of the same experiment."""
        self.name = name
        self.groups = sorted(groups, key=lambda g: g.group_type)
        self.num_groups = len(self.groups)

    def get_group_type_to_df(self) -> Dict[str, pd.DataFrame]:
        return {g.group_type: g.get_df() for g in self.groups}
