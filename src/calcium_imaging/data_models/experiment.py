from pathlib import Path
from typing import List, Dict, Iterator, Union

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

from calcium_imaging.ui import get_bool_input, get_int_input
from calcium_imaging.viz import create_traces_figure, get_n_colors_from_palette
from .group import Group
from .roi import ROI


class Experiment:
    """A folder containing multiple Conditions, e.g., 'SI_SH_check'."""

    def __init__(self, name: str, groups: List[Group]) -> None:
        """Holds multiple groups of the same experiment."""
        self.name = name
        self.groups = sorted(groups, key=lambda g: g.group_type)
        self._id2group = {g.group_type: g for g in self.groups}
        self.num_groups = len(self.groups)
        self.num_rois = len([roi for roi in self.iter_rois()])

    def __getitem__(self, group_type: str) -> Group:
        return self._id2group[group_type]

    def __len__(self) -> int:
        return len(self.groups)

    def __iter__(self) -> Iterator[Group]:
        return iter(self.groups)

    def visualize(self) -> None:
        colors = get_n_colors_from_palette(self.num_groups)

        all_traces = []
        max_trace_val = 0
        for color, group in zip(colors, self.groups):
            rois_traces = [roi.trace for cs in group for roi in cs]
            average_trace = pd.Series(pd.concat(rois_traces, axis=1).mean(axis=1))
            average_trace.name = f"{group.group_type} mean"
            if average_trace.max() > max_trace_val:
                max_trace_val = average_trace.max()
            group_fig = create_traces_figure(
                main_trace=average_trace,
                traces_color=color
            )
            all_traces.append(group_fig.data[0])

        # Combine all traces into one figure
        fig = go.Figure(data=all_traces)
        fig.update_layout(
            title=self.name,
            xaxis_title="Frame",
            yaxis_title="Fluorescence relative to background",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            template="plotly_white",
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.05,
                font=dict(size=10),
                traceorder="normal",
            ),
        )
        fig.show()

    def visualize_all_rois(self) -> None:
        for roi in self.iter_rois():
            try:
                roi.visualize()
            except Exception as e:
                print(e)
                print(f"consider exp['{roi.group_type}'][{roi.coverslip_id}].drop(roi_id={roi.roi_id})")
                print("fallback visualization: ")
                roi.trace.plot()
                plt.title(roi.title)
                plt.show()

    def run_manual_analysis(self) -> None:
        for i, roi in enumerate(self.iter_rois()):
            try:
                print(f"ROI {i}/{self.num_rois}")
                self._ask_to_update_params(roi)
            except Exception as e:
                print(e)
                print("fallback visualization: ")
                roi.trace.plot()
                plt.title(roi.title)
                plt.show()
                drop = get_bool_input("drop ROI? (y/n): ")
                if drop:
                    msg = f"deleted {roi.title}"
                    del roi
                    print(msg)
                else:
                    self._ask_to_update_params(roi)

    @staticmethod
    def _ask_to_update_params(roi: ROI):
        while True:
            roi.visualize()
            peak_idx = get_int_input(f"peak_idx={roi.peak_idx}, enter to accept or input to edit: ")
            if peak_idx is not None:
                roi.set_peak_idx(peak_idx)

            onset_idx = get_int_input(f"onset_idx={roi.onset_idx}, enter to accept or input to edit: ")
            if onset_idx is not None:
                roi.set_onset_idx(onset_idx)

            if peak_idx is not None or onset_idx is not None:
                roi.visualize()
            else:
                break

    def calculate_eflux_rates(self, return_json: bool = False) -> Union[List[float], List[Dict[str, float]]]:
        return [
            eflux_rate
            for group in self.groups
            for eflux_rate in group.calculate_eflux_rates(return_json=return_json)
        ]

    def calculate_amplitudes(self, return_json: bool = False) -> Union[List[float], List[Dict[str, float]]]:
        return [
            amplitude
            for group in self.groups
            for amplitude in group.calculate_amplitudes(return_json=return_json)
        ]

    def get_group_type_to_df(self) -> Dict[str, pd.DataFrame]:
        return {g.group_type: g.get_df() for g in self.groups}

    def save_mega_dfs(self, results_output_dir_path: str = "./results") -> None:  # todo handle i/o better
        results_output_dir_path = Path(results_output_dir_path) / self.name
        results_output_dir_path.mkdir(parents=True, exist_ok=True)
        for group_type, df in self.get_group_type_to_df().items():
            base = results_output_dir_path / group_type
            df.to_excel(base.with_suffix(".xlsx"), index=False)
            df.to_csv(base.with_suffix(".csv"), index=False)
        print(f"Successfully saved {self.num_groups} mega dfs to {results_output_dir_path.resolve()}")

    def iter_rois(self) -> Iterator[ROI]:
        for group in self.groups:
            for coverslip in group.coverslips:
                for roi in coverslip.rois:
                    yield roi

