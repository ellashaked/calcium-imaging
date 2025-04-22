from pathlib import Path
from typing import List

from .data_models import Coverslip, ExperimentalCondition, Experiment
from .io import load_coverslip, validate_experiment_dir


def _instantiate_coverslips(experiment_dir_path: Path) -> List[Coverslip]:
    coverslips = [
        Coverslip(*load_coverslip(coverslip_file_path)).preprocess()
        for coverslip_file_path in experiment_dir_path.iterdir()
    ]
    return coverslips


def _instantiate_experimental_conditions(coverslips_list: List[Coverslip]) -> List[ExperimentalCondition]:
    unique_experimental_condition_types = sorted(set(cs.experimental_condition_type for cs in coverslips_list))
    experimental_conditions_list = []
    for condition_type in unique_experimental_condition_types:
        relevant_runs = [
            coverslip for coverslip in coverslips_list
            if coverslip.experimental_condition_type == condition_type
        ]
        new_experimental_condition = ExperimentalCondition(
            condition_type=condition_type,
            coverslips_list=relevant_runs
        )
        experimental_conditions_list.append(new_experimental_condition)
    return experimental_conditions_list


def _instantiate_experiment(
        experiment_name: str,
        experimental_conditions_list: List[ExperimentalCondition]
) -> Experiment:
    experiment = Experiment(
        name=experiment_name,
        experimental_conditions_list=experimental_conditions_list
    )
    return experiment


def load_experiment_from_dir(experiment_dir: str) -> Experiment:
    """Reads an experiment directory and parses it into an Experiment class object"""
    experiment_dir_path = validate_experiment_dir(experiment_dir)
    coverslips = _instantiate_coverslips(experiment_dir_path)
    experimental_conditions = _instantiate_experimental_conditions(coverslips)
    experiment = _instantiate_experiment(
        experiment_name=experiment_dir_path.stem,
        experimental_conditions_list=experimental_conditions
    )
    return experiment
