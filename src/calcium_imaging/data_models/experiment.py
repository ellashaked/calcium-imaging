from pathlib import Path
from typing import List, Dict, Iterator, Union

import pandas as pd

from .group import Group


class Experiment:
    """A folder containing multiple Conditions, e.g., 'SI_SH_check'."""

    def __init__(self, name: str, groups: List[Group]) -> None:
        """Holds multiple groups of the same experiment."""
        self.name = name
        self.groups = sorted(groups, key=lambda g: g.group_type)
        self._id2group = {g.group_type: g for g in self.groups}
        self.num_groups = len(self.groups)

    def __getitem__(self, group_type: str) -> Group:
        return self._id2group[group_type]

    def __len__(self) -> int:
        return len(self.groups)

    def __iter__(self) -> Iterator[Group]:
        return iter(self.groups)

    def calculate_eflux_rates(self, return_json: bool = False) -> Union[List[float], List[Dict[str, float]]]:
        return [
            eflux_rate
            for group in self.groups
            for eflux_rate in group.calculate_eflux_rates(return_json=return_json)
        ]

    def calculate_amplitudes(self, return_json: bool = False) -> Union[List[float], List[Dict[str, float]]]:
        return [
            amplitude
            for group in self.groups
            for amplitude in group.calculate_amplitudes(return_json=return_json)
        ]

    def get_group_type_to_df(self) -> Dict[str, pd.DataFrame]:
        return {g.group_type: g.get_df() for g in self.groups}

    def save_mega_dfs(self, results_output_dir_path: str = "./results") -> None:  # todo handle i/o better
        results_output_dir_path = Path(results_output_dir_path) / self.name
        results_output_dir_path.mkdir(parents=True, exist_ok=True)
        for group_type, df in self.get_group_type_to_df().items():
            base = results_output_dir_path / group_type
            df.to_excel(base.with_suffix(".xlsx"), index=False)
            df.to_csv(base.with_suffix(".csv"), index=False)
        print(f"Successfully saved {self.num_groups} mega dfs to {results_output_dir_path.resolve()}")
