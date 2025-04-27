from typing import Dict, List

import pandas as pd

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

    def get_df(self) -> pd.DataFrame:
        return pd.concat([roi.series for roi in self.rois], axis=1)

    @staticmethod
    def _init_rois(rois: List[ROI]) -> List[ROI]:
        rois = sorted(rois, key=lambda roi: roi.roi_id)
        if len(rois) == 0:
            raise ValueError(f"Initializing class Coverslip with empty ROIs list is illegal.")
        if not all([roi.coverslip_id == rois[0].coverslip_id for roi in rois]):
            raise ValueError(f"All ROIs must share the same coverslip ID.")
        return rois
