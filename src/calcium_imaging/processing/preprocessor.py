from typing import List

import pandas as pd
from scipy.signal import find_peaks

from .constants import BACKGROUND_FLUORESCENCE_ROIS, TIME_COL


class Preprocessor:
    def __init__(
            self,
            first_n_points_to_discard: int = 5,
            smoothing_windows_size: int = 2,
            time_col_name: str = TIME_COL,
            background_fluorescence_cols_names: List[str] = BACKGROUND_FLUORESCENCE_ROIS,
            normalization_sampling_start_frame: int = 1,
            normalization_sampling_end_frame: int = 35,
            earliest_onset_frame: int = 50,
            earliest_baseline_recovery_frame: int = 90,
            drop_traces_with_corrupted_peak: bool = False,
            drop_background_fluorescence_cols: bool = True
    ) -> None:
        self.first_n_points_to_discard = first_n_points_to_discard
        self.smoothing_windows_size = smoothing_windows_size
        self.time_col_name = time_col_name
        self.background_fluorescence_cols_names = background_fluorescence_cols_names
        self.normalization_sampling_start_frame = normalization_sampling_start_frame
        self.normalization_sampling_end_frame = normalization_sampling_end_frame
        self.earliest_onset_frame = earliest_onset_frame
        self.earliest_baseline_recovery_frame = earliest_baseline_recovery_frame
        self.drop_traces_with_corrupted_peak = drop_traces_with_corrupted_peak
        self.drop_background_fluorescence_cols = drop_background_fluorescence_cols

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy(deep=True)
        df = self.discard_first_n_points(df, n=self.first_n_points_to_discard)
        df = self.smoothen(df, window_size=self.smoothing_windows_size)
        df = self.subtract_baseline_fluorescence(df, self.background_fluorescence_cols_names)
        if self.drop_background_fluorescence_cols:
            df = df.drop(columns=self.background_fluorescence_cols_names)
        df = self.normalize(
            df=df,
            sampling_start_frame=self.normalization_sampling_start_frame,
            sampling_end_frame=self.normalization_sampling_end_frame
        )
        df = self._detect_traces_with_corrupted_peak(df, drop=self.drop_traces_with_corrupted_peak)
        return df

    @staticmethod
    def discard_first_n_points(df: pd.DataFrame, n: int) -> pd.DataFrame:
        return df.iloc[n:]

    @staticmethod
    def smoothen(df: pd.DataFrame, window_size: int = 2) -> pd.DataFrame:
        """Assuming df includes only cell ROIs (no dead / fluorescence background) ROIs or time cols"""
        return df.rolling(
            window=window_size,
            min_periods=1,  # allow smaller windows at edges
            center=True
        ).mean()

    @staticmethod
    def subtract_baseline_fluorescence(df: pd.DataFrame, background_roi_cols: List[str]) -> pd.DataFrame:
        averaged = df[background_roi_cols].mean(axis=1)
        result_df = df.subtract(averaged, axis=0)
        return result_df

    @staticmethod
    def normalize(df: pd.DataFrame, sampling_start_frame: int = 1, sampling_end_frame: int = 35) -> pd.DataFrame:
        """Assuming df includes only cell ROIs (no dead / fluorescence background) ROIs or time cols"""
        f0 = df.iloc[sampling_start_frame:sampling_end_frame].mean(axis=0)  # baseline fluorescence
        result_df = df.div(f0, axis=1)
        return result_df

    @staticmethod
    def reject_noise(
            df: pd.DataFrame,
            *,
            start_index: int = 35,
            factor_mean: float = 7.0,
            factor_peak: float = 2.0,
            overshoot_thresh: float = 2.0,
            overshoot_repl: float = 3.0,
    ) -> pd.DataFrame:
        """
        Drop columns considered artifactual.

        Criteria (mirrors original MATLAB logic):

        1. Global peak occurs before the rising point  → remove column.
        2. Pre-rise segment too noisy (see `noisy_pre_rise`)            → remove.
        3. Overshoot spikes above threshold are *corrected* in-place
           before criteria 1–2 are evaluated.

        Returns
        -------
        pd.DataFrame
            Cleaned dataframe with offending columns removed.
        """
        cleaned = df.copy(deep=True)

        for col in cleaned.columns:
            s = cleaned[col]

            # step-wise overshoot correction (in-place)
            cleaned[col] = Preprocessor.correct_overshoot(
                s,
                factor_threshold=overshoot_thresh,
                factor_replacement=overshoot_repl,
            )

            if Preprocessor.noisy_pre_rise(
                    cleaned[col], factor_mean, factor_peak, start_index
            ):
                cleaned.drop(columns=[col], inplace=True)

        return cleaned

    # ------------------------------------------------------------------
    def _detect_traces_with_corrupted_peak(self, df: pd.DataFrame, drop: bool = False) -> pd.DataFrame:
        """True if the global maximum is located *before* `start_index`."""
        result_df = df.copy(deep=True)
        for col, trace in df.items():
            idx_max = trace.index.values[trace.argmax()]
            if idx_max < self.earliest_onset_frame:
                if drop:
                    result_df = result_df.drop(columns=[col])
                print(f"   warning {col}: peak detected before frame {self.earliest_onset_frame}, drop={drop}")
            if idx_max > self.earliest_baseline_recovery_frame:
                print(f"   warning {col}: peak detected after frame {self.earliest_baseline_recovery_frame}, drop={drop}")
                if drop:
                    result_df = result_df.drop(columns=[col])
        return result_df

    # ------------------------------------------------------------------
    @staticmethod
    def correct_overshoot(
            trace: pd.Series,
            factor_threshold: float,
            factor_replacement: float,
            pre_window: int = 35,
    ) -> pd.Series:
        """
        Clamp samples whose value exceeds
            smooth + factor_threshold * mean_pre_peaks
        to
            smooth + factor_replacement * mean_pre_peaks.

        The moving-average of the trace (window=10) is used as the
        “smooth” estimate.
        """
        if trace.isna().all():
            return trace

        smooth = trace.rolling(window=10, center=True, min_periods=1).mean()
        # peaks only in the pre-rise region
        peaks, _ = find_peaks(trace.iloc[:pre_window])
        mean_pre_peaks = trace.iloc[peaks].mean() if peaks.size else 0.0

        threshold = smooth + factor_threshold * mean_pre_peaks
        replacement = smooth + factor_replacement * mean_pre_peaks

        corrected = trace.where(trace <= threshold, replacement)
        return corrected

    # ------------------------------------------------------------------
    @staticmethod
    def noisy_pre_rise(
            trace: pd.Series,
            factor_mean: float,
            factor_peak: float,
            start_index: int = 35,
    ) -> bool:
        """
        Returns *True* if the pre-rise segment is noisy per MATLAB rules.

        Rule 1 – mean(pre-segment peaks) · factor_mean  > global_max
        Rule 2 – max(pre-segment peaks)  · factor_peak  > global_max
        """
        if trace.isna().all():
            return True

        pre_segment = trace.iloc[:start_index]
        peaks, _ = find_peaks(pre_segment)

        if peaks.size == 0:
            return False  # no peaks ⇒ not noisy by this definition

        peaks_vals = pre_segment.iloc[peaks]
        global_max = trace.max()

        condition1 = peaks_vals.mean() * factor_mean > global_max
        condition2 = peaks_vals.max() * factor_peak > global_max
        return condition1 or condition2
