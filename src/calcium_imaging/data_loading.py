from pathlib import Path

from .data_models import Run, Condition, Experiment
from .io import load_run


def load_experiment_from_dir(experiment_dir_path: Path):
    """Reads an experiment directory and parses it into an Experiment class object"""
    runs = [
        Run(*load_run(run_file_path))
        for run_file_path in experiment_dir_path.iterdir()
    ]
    unique_conditions = sorted(set(run.condition_type for run in runs))
    experiment_conditions = []
    for condition_type in unique_conditions:
        relevant_runs = [run for run in runs if run.condition_type == condition_type]
        new_condition = Condition(
            condition_type=condition_type,
            runs_list=relevant_runs
        )
        experiment_conditions.append(new_condition)
    experiment = Experiment(
        name=experiment_dir_path.stem,
        conditions_list=experiment_conditions
    )
    return experiment
