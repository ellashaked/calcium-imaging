from typing import List, Iterator, Dict
import pandas as pd
from pathlib import Path

from .experiment import Experiment


class Research:
    """A collection of multiple experiments."""

    def __init__(self, name: str, experiments: List[Experiment]) -> None:
        """Holds multiple experiments of the same research project."""
        self.name = name
        self.experiments = sorted(experiments, key=lambda e: e.name)
        self._id2experiment = {e.name: e for e in self.experiments}
        self.num_experiments = len(self.experiments)
        self.num_groups = sum(e.num_groups for e in self.experiments)
        self.num_rois = sum(e.num_rois for e in self.experiments)
        self.title = f"{name} (Experiments {', '.join([e.name for e in self.experiments])})"

    def __getitem__(self, experiment_name: str) -> Experiment:
        return self._id2experiment[experiment_name]

    def __len__(self) -> int:
        return len(self.experiments)

    def __iter__(self) -> Iterator[Experiment]:
        return iter(self.experiments)

    def __repr__(self) -> str:
        return self.title

    def get_full_analysis_df(self) -> pd.DataFrame:
        """Get a combined DataFrame of all experiments' analysis results."""
        dfs = [experiment.get_full_analysis_df() for experiment in self.experiments]
        df = pd.concat(dfs, axis=0)
        df = df.sort_values(by=["experiment_name", "group_type", "coverslip", "roi"], ascending=True)
        df = df.reset_index(drop=True)
        return df

    def save_mega_dfs(self, results_output_dir_path: str = "./results") -> None:
        """Save analysis results for all experiments."""
        results_output_dir_path = Path(results_output_dir_path) / self.name
        results_output_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Save individual experiment results
        for experiment in self.experiments:
            experiment.save_mega_dfs(results_output_dir_path)
        
        # Save combined results
        combined_df = self.get_full_analysis_df()
        base = results_output_dir_path / "combined_analysis"
        combined_df.to_excel(base.with_suffix(".xlsx"), index=False)
        combined_df.to_csv(base.with_suffix(".csv"), index=False)
        print(f"Successfully saved combined analysis to {results_output_dir_path.resolve()}") 