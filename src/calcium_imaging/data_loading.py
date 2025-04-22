from pathlib import Path

from .data_models import Coverslip, ExperimentalCondition, Experiment
from .io import load_coverslip


def load_experiment_from_dir(experiment_dir_path: Path):
    """Reads an experiment directory and parses it into an Experiment class object"""
    coverslips = [
        Coverslip(*load_coverslip(coverslip_file_path)).preprocess()
        for coverslip_file_path in experiment_dir_path.iterdir()
    ]
    unique_experimental_condition_types = sorted(set(cs.experimental_condition_type for cs in coverslips))
    experimental_conditions_list = []
    for condition_type in unique_experimental_condition_types:
        relevant_runs = [
            coverslip for coverslip in coverslips
            if coverslip.experimental_condition_type == condition_type
        ]
        new_experimental_condition = ExperimentalCondition(
            condition_type=condition_type,
            coverslips_list=relevant_runs
        )
        experimental_conditions_list.append(new_experimental_condition)
    experiment = Experiment(
        name=experiment_dir_path.stem,
        experimental_conditions_list=experimental_conditions_list
    )
    return experiment
