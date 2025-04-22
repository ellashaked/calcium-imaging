from pathlib import Path

from .data_loading import load_experiment_from_dir


def validate_experiment_dir(experiment_dir: str) -> Path:
    experiment_dir_path = Path(experiment_dir)
    if not experiment_dir_path.exists():
        raise ValueError(f"experiment_dir '{experiment_dir}' doesn't exist.")
    if not experiment_dir_path.is_dir():
        raise ValueError(f"experiment_dir '{experiment_dir}' is not a directory.")
    return experiment_dir_path


def run_analysis(experiment_dir: str) -> None:
    experiment_dir_path = validate_experiment_dir(experiment_dir)
    experiment = load_experiment_from_dir(experiment_dir_path)
    print()
