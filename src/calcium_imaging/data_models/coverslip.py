from typing import Dict, List, Iterator, Union, Callable, Optional

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

    def __repr__(self) -> str:
        return self.name

    def __getitem__(self, roi_id: int) -> ROI:
        return self._id2roi[roi_id]

    def __len__(self) -> int:
        return len(self.rois)

    def __iter__(self) -> Iterator[ROI]:
        return iter(self.rois)

    def get_df(self) -> pd.DataFrame:
        return pd.concat([roi.trace for roi in self.rois], axis=1)

    def visualize(self, title_prefix: Optional[str] = None) -> None:
        rois_traces = [roi.trace for roi in self.rois]
        average_trace = pd.Series(pd.concat(rois_traces, axis=1).mean(axis=1))
        average_trace.name = f"Coverslip {self.id} mean"
        base_title = f"Coverslip {self.id} ({self.group_type})"
        create_traces_figure(
            main_trace=average_trace,
            additional_traces=rois_traces,
            title=base_title if title_prefix is None else f"{title_prefix}\n{base_title}",
            xaxis_title="Frame",
            yaxis_title="Fluorescence relative to background",
            yaxis_range=(0.5, max(2.5, average_trace.max())),
        ).show()

    def _calculate_metric(
            self,
            metric_calculation_func: Callable[['ROI'], float],
            metric_name: str,
            return_json: bool
    ) -> Union[List[float], List[Dict[str, float]]]:
        # first, compute all the raw values
        values = [metric_calculation_func(roi) for roi in self.rois]

        if not return_json:
            return values

        # otherwise build the JSON objects
        return [
            {
                "group_type": self.group_type,
                "coverslip": roi.coverslip_id,
                "roi": roi.roi_id,
                metric_name: val
            }
            for roi, val in zip(self.rois, values)
        ]

    def calculate_eflux_rates(self, return_json: bool = False) -> Union[List[float], List[Dict[str, float]]]:
        return self._calculate_metric(
            lambda roi: roi.calculate_eflux(),
            metric_name="eflux",
            return_json=return_json
        )

    def calculate_amplitudes(self, return_json: bool = False) -> Union[List[float], List[Dict[str, float]]]:
        return self._calculate_metric(
            lambda roi: roi.calculate_amplitude(),
            metric_name="amplitude",
            return_json=return_json
        )

    @staticmethod
    def _init_rois(rois: List[ROI]) -> List[ROI]:
        rois = sorted(rois, key=lambda roi: roi.roi_id)
        if len(rois) == 0:
            raise ValueError(f"Initializing class Coverslip with empty ROIs list is illegal.")
        if not all([roi.coverslip_id == rois[0].coverslip_id for roi in rois]):
            raise ValueError(f"All ROIs must share the same coverslip ID.")
        return rois
