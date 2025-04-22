from pathlib import Path


def validate_experiment_dir(experiment_dir: str) -> Path:
    experiment_dir_path = Path(experiment_dir)
    if not experiment_dir_path.exists():
        raise ValueError(f"experiment_dir '{experiment_dir}' doesn't exist.")
    if not experiment_dir_path.is_dir():
        raise ValueError(f"experiment_dir '{experiment_dir}' is not a directory.")
    return experiment_dir_path
