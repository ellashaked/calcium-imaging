from .data_loading import load_experiment_from_dir
from .io import validate_experiment_dir


def run_analysis(experiment_dir: str) -> None:
    experiment_dir_path = validate_experiment_dir(experiment_dir)
    experiment = load_experiment_from_dir(experiment_dir_path)
    print()
