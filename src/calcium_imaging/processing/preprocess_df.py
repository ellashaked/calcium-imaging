import pandas as pd

from calcium_imaging.constants import BACKGROUND_FLUORESCENCE_ROIS, TIME_COL
from .discard_first_n_points import discard_first_n_points
from .normalize import normalize
from .rename_columns import rename_columns
from .smoothen import smoothen
from .subtract_background_fluorescence import subtract_background_fluorescence


def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:  # todo magic numbers
    df = discard_first_n_points(df, n=5)
    df = smoothen(df, window_size=2)
    df = subtract_background_fluorescence(df, BACKGROUND_FLUORESCENCE_ROIS)
    df = df.drop(columns=[TIME_COL] + BACKGROUND_FLUORESCENCE_ROIS)
    df = normalize(df, sampling_start_frame=1, sampling_end_frame=35)
    df = rename_columns(df, f"cs-{id}")
    return df
