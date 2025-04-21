from pathlib import Path
from typing import Union

from .data_loading import load_experiment_from_dir


def run_analysis(experiment_dir: Union[str, Path]) -> None:
    experiment_dir_path = Path(experiment_dir)
    if not experiment_dir_path.exists():
        raise ValueError(f"experiment_dir '{experiment_dir}' doesn't exist.")
    if not experiment_dir_path.is_dir():
        raise ValueError(f"experiment_dir '{experiment_dir}' is not a directory.")
    experiment = load_experiment_from_dir(experiment_dir_path)
    print()
