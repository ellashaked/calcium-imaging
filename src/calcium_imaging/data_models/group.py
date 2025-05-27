from typing import List, Iterator, Dict, Optional

import numpy as np
import pandas as pd

from calcium_imaging.viz import create_traces_figure
from .coverslip import Coverslip


class Group:
    """One group with certain intervention, e.g. 'shNCLX'."""

    def __init__(self, coverslips: List[Coverslip]) -> None:
        """Holds multiple runs of the same group"""
        self.coverslips = self._init_coverslips(coverslips)
        self._id2coverslip = {cs.id: cs for cs in self.coverslips}
        self.group_type = self._infer_group_type()
        self.title = f"{self.group_type} (Coverslips {', '.join([str(cs.id) for cs in self.coverslips])})"

    def get_df(self) -> pd.DataFrame:
        return pd.concat([cs.get_df() for cs in self.coverslips], axis=1)

    def __repr__(self) -> str:
        return self.title

    def __getitem__(self, coverslip_id: int) -> Coverslip:
        return self._id2coverslip[coverslip_id]

    def __len__(self) -> int:
        return len(self.coverslips)

    def __iter__(self) -> Iterator[Coverslip]:
        return iter(self.coverslips)

    def visualize(self, title_prefix: Optional[str] = None) -> None:
        rois_traces = [roi.trace for cs in self.coverslips for roi in cs]
        rois_peak_indexes = [roi.peak_idx for cs in self.coverslips for roi in cs]
        rois_onset_indexes = [roi.onset_idx for cs in self.coverslips for roi in cs]
        average_trace = pd.Series(pd.concat(rois_traces, axis=1).mean(axis=1))
        average_trace.name = f"{self.group_type} mean"
        base_title = f"{self.group_type} (Coverslips {', '.join([str(cs.id) for cs in self.coverslips])})"
        create_traces_figure(
            main_trace=average_trace,
            additional_traces=rois_traces,
            additional_traces_peak_indexes=rois_peak_indexes,
            additional_traces_onset_indexes=rois_onset_indexes,
            title=base_title if title_prefix is None else f"{title_prefix}\n{base_title}",
            xaxis_title="Frame",
            yaxis_title="Fluorescence relative to background",
        ).show()

    def calculate_eflux_rates(self) -> List[Dict[str, float]]:
        return [
            eflux_rate
            for cs in self.coverslips
            for eflux_rate in cs.calculate_eflux_rates()
        ]

    def calculate_amplitudes(self) -> List[Dict[str, float]]:
        return [
            amplitude
            for cs in self.coverslips
            for amplitude in cs.calculate_amplitudes()
        ]

    def align_onsets(self, target_onset_idx: Optional[int] = None) -> None:
        if target_onset_idx is None:
            onset_indexes = [roi.onset_idx for cs in self.coverslips for roi in cs]
            target_onset_idx = int(np.median(onset_indexes))
            print(f"aligning {len(onset_indexes)} ROIs to {target_onset_idx}")
        for coverslip in self.coverslips:
            for roi in coverslip.rois:
                roi.shift_trace(target_onset_idx - roi.onset_idx)

    @staticmethod
    def _init_coverslips(coverslips: List[Coverslip]) -> List[Coverslip]:
        coverslips = sorted(coverslips, key=lambda cs: cs.id)
        if len(coverslips) == 0:
            raise ValueError(f"Initializing class Group with empty Coverslips list is illegal.")
        if not all([cs.group_type == coverslips[0].group_type for cs in coverslips]):
            raise ValueError(f"All Coverslips must share the same group type.")
        return coverslips

    def _infer_group_type(self) -> str:
        return self.coverslips[0].group_type
