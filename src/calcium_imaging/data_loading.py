from pathlib import Path

from .data_models import Coverslip, Condition, Experiment
from .io import load_coverslip


def load_experiment_from_dir(experiment_dir_path: Path):
    """Reads an experiment directory and parses it into an Experiment class object"""
    coverslips = [
        Coverslip(*load_coverslip(coverslip_file_path)).preprocess()
        for coverslip_file_path in experiment_dir_path.iterdir()
    ]
    unique_conditions = sorted(set(coverslip.condition_type for coverslip in coverslips))
    experiment_conditions = []
    for condition_type in unique_conditions:
        relevant_runs = [coverslip for coverslip in coverslips if coverslip.condition_type == condition_type]
        new_condition = Condition(
            condition_type=condition_type,
            coverslips_list=relevant_runs
        )
        experiment_conditions.append(new_condition)
    experiment = Experiment(
        name=experiment_dir_path.stem,
        conditions_list=experiment_conditions
    )
    return experiment
