from typing import Dict, List, Iterator, Union, Callable, Optional

import numpy as np
import pandas as pd

from calcium_imaging.viz import create_traces_figure
from .roi import ROI


class Coverslip:
    """One plate"""

    def __init__(self, coverslip_id: int, group_type: str, rois: List[ROI]) -> None:
        self.rois = self._init_rois(rois)
        self._id2roi = {roi.roi_id: roi for roi in self.rois}
        self.id = coverslip_id
        self.group_type = group_type
        self.name = f"cs-{self.id}"
        self.title = f"Coverslip {self.id} (ROIs {', '.join(str(roi.roi_id) for roi in self.rois)})"

    def __repr__(self) -> str:
        return self.title

    def __getitem__(self, roi_id: int) -> ROI:
        return self._id2roi[roi_id]

    def __len__(self) -> int:
        return len(self.rois)

    def __iter__(self) -> Iterator[ROI]:
        return iter(self.rois)

    def drop_roi(self, roi_id: int) -> None:
        try:
            self._id2roi.pop(roi_id)
            self.rois = [roi for roi in self.rois if roi.roi_id != roi_id]
            print(f"Successfully dropped ROI {roi_id} from Coverslip {self.id}")
        except KeyError:
            print(f"ROI with id {roi_id} not found in '{self.name}'")

    def get_df(self) -> pd.DataFrame:
        return pd.concat([roi.trace for roi in self.rois], axis=1)

    def visualize(self, title_prefix: Optional[str] = None) -> None:
        rois_traces = [roi.trace for roi in self.rois]
        rois_peak_indexes = [roi.peak_idx for roi in self.rois]
        rois_onset_indexes = [roi.onset_idx for roi in self.rois]
        average_trace = pd.Series(pd.concat(rois_traces, axis=1).mean(axis=1))
        average_trace.name = f"Coverslip {self.id} mean"
        base_title = f"Coverslip {self.id} ({self.group_type})"
        create_traces_figure(
            main_trace=average_trace,
            additional_traces=rois_traces,
            additional_traces_peak_indexes=rois_peak_indexes,
            additional_traces_onset_indexes=rois_onset_indexes,
            title=base_title if title_prefix is None else f"{title_prefix}\n{base_title}",
            xaxis_title="Frame",
            yaxis_title="Fluorescence relative to background",
        ).show()

    def _calculate_metric(
            self,
            metric_calculation_func: Callable[['ROI'], float],
            metric_name: str,
    ) -> Union[List[float], List[Dict[str, float]]]:
        return [
            {
                "group_type": self.group_type,
                "coverslip": roi.coverslip_id,
                "roi": roi.roi_id,
                metric_name: metric_calculation_func(roi)
            }
            for roi in self.rois
        ]

    def calculate_eflux_rates(self) -> List[Dict[str, float]]:
        return self._calculate_metric(
            lambda roi: roi.calculate_eflux(),
            metric_name="eflux",
        )

    def calculate_amplitudes(self) -> List[Dict[str, float]]:
        return self._calculate_metric(
            lambda roi: roi.calculate_amplitude(),
            metric_name="amplitude",
        )

    def calculate_integrals(self) -> List[Dict[str, float]]:
        return self._calculate_metric(
            lambda roi: roi.calculate_integral(),
            metric_name="integral",
        )

    def align_onsets(self, target_onset_idx: Optional[int] = None) -> None:
        if target_onset_idx is None:
            target_onset_idx = int(np.median([roi.onset_idx for roi in self.rois]))
            print(f"aligning {len(self.rois)} ROIs to {target_onset_idx}")
        for roi in self.rois:
            roi.shift_trace(target_onset_idx - roi.onset_idx)

    @staticmethod
    def _init_rois(rois: List[ROI]) -> List[ROI]:
        rois = sorted(rois, key=lambda roi: roi.roi_id)
        if len(rois) == 0:
            raise ValueError(f"Initializing class Coverslip with empty ROIs list is illegal.")
        if not all([roi.coverslip_id == rois[0].coverslip_id for roi in rois]):
            raise ValueError(f"All ROIs must share the same coverslip ID.")
        return rois
