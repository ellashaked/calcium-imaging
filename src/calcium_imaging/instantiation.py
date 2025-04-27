from pathlib import Path
from typing import List

import pandas as pd

from .processing import Preprocessor, extract_roi_id_from_col_name, extract_coverslip_info_from_filename_stem
from .data_models import ROI, Coverslip, Group, Experiment
from .io import load_vsi, validate_experiment_dir


def _instantiate_preprocessor() -> Preprocessor:
    return Preprocessor(
        first_n_points_to_discard=5,
        smoothing_windows_size=2,
        normalization_sampling_start_frame=1,
        normalization_sampling_end_frame=35,
        drop_time_col=True,
        drop_background_fluorescence_cols=True,
    )


def _instantiate_rois(coverslip_id: int, df: pd.DataFrame, preprocessor: Preprocessor) -> List[ROI]:
    return sorted([
        ROI(
            coverslip_id=coverslip_id,
            roi_id=extract_roi_id_from_col_name(str(col_name)),
            series=series
        )
        for col_name, series in preprocessor.preprocess(df).iteritems()
    ], key=lambda x: x.roi_id)


def _instantiate_coverslips(experiment_dir_path: Path, preprocessor: Preprocessor) -> List[Coverslip]:
    coverslips = []
    for coverslip_file_path in experiment_dir_path.iterdir():
        try:
            df = load_vsi(coverslip_file_path)
            coverslip_info = extract_coverslip_info_from_filename_stem(coverslip_file_path.stem)
            rois = _instantiate_rois(
                coverslip_id=coverslip_info.coverslip_id,
                df=df,
                preprocessor=preprocessor
            )
            coverslip = Coverslip(
                coverslip_id=coverslip_info.coverslip_id,
                group_type=coverslip_info.group_type,
                rois=rois
            )
            coverslips.append(coverslip)
        except ValueError:
            print(f"Error loading {coverslip_file_path.resolve()}, skipping.")
    return coverslips


def _instantiate_groups(coverslips: List[Coverslip]) -> List[Group]:
    unique_group_types = sorted(set(cs.group_type for cs in coverslips))
    groups = []
    for group_type in unique_group_types:
        relevant_runs = [
            coverslip for coverslip in coverslips
            if coverslip.group_type == group_type
        ]
        group = Group(coverslips=relevant_runs)
        groups.append(group)
    return groups


def _instantiate_experiment(
        experiment_name: str,
        groups: List[Group]
) -> Experiment:
    experiment = Experiment(
        name=experiment_name,
        groups=groups
    )
    return experiment


def load_experiment_from_dir(experiment_dir: str) -> Experiment:
    """Reads an experiment directory and parses it into an Experiment class object"""
    experiment_dir_path = validate_experiment_dir(experiment_dir)
    preprocessor = _instantiate_preprocessor()
    coverslips = _instantiate_coverslips(experiment_dir_path, preprocessor)
    groups = _instantiate_groups(coverslips)
    experiment = _instantiate_experiment(
        experiment_name=experiment_dir_path.stem,
        groups=groups
    )
    return experiment
