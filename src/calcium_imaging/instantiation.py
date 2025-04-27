from pathlib import Path
from typing import List

from .data_models import Coverslip, Group, Experiment
from .io import load_coverslip, validate_experiment_dir


def _instantiate_coverslips(experiment_dir_path: Path) -> List[Coverslip]:
    coverslips = []
    for coverslip_file_path in experiment_dir_path.iterdir():
        try:
            name, df = load_coverslip(coverslip_file_path)
            coverslip = Coverslip(name, df).preprocess()
            coverslips.append(coverslip)
        except ValueError:
            print(f"Error loading {coverslip_file_path.resolve()}, skipping.")
    return coverslips


def _instantiate_groups(coverslips_list: List[Coverslip]) -> List[Group]:
    unique_group_types = sorted(set(cs.group_type for cs in coverslips_list))
    groups_list = []
    for group_type in unique_group_types:
        relevant_runs = [
            coverslip for coverslip in coverslips_list
            if coverslip.group_type == group_type
        ]
        new_group = Group(
            group_type=group_type,
            coverslips=relevant_runs
        )
        groups_list.append(new_group)
    return groups_list


def _instantiate_experiment(
        experiment_name: str,
        groups_list: List[Group]
) -> Experiment:
    experiment = Experiment(
        name=experiment_name,
        groups=groups_list
    )
    return experiment


def load_experiment_from_dir(experiment_dir: str) -> Experiment:
    """Reads an experiment directory and parses it into an Experiment class object"""
    experiment_dir_path = validate_experiment_dir(experiment_dir)
    coverslips = _instantiate_coverslips(experiment_dir_path)
    groups = _instantiate_groups(coverslips)
    experiment = _instantiate_experiment(
        experiment_name=experiment_dir_path.stem,
        groups_list=groups
    )
    return experiment
