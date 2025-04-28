from pathlib import Path
from typing import Union


def validate_experiment_dir(experiment_dir: Union[str, Path]) -> Path:
    if isinstance(experiment_dir, str):
        experiment_dir_path = Path(experiment_dir)
    elif isinstance(experiment_dir, Path):
        experiment_dir_path = experiment_dir
    else:
        raise ValueError(f"Illegal type {type(experiment_dir)} for experiment_dir. "
                         f"Provide either str or Path.")
    if not experiment_dir_path.exists():
        raise ValueError(f"experiment_dir '{experiment_dir}' doesn't exist.")
    if not experiment_dir_path.is_dir():
        raise ValueError(f"experiment_dir '{experiment_dir}' is not a directory.")
    return experiment_dir_path
