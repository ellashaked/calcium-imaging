from typing import Optional

import pandas as pd
import numpy as np

from calcium_imaging.analysis import (
    calculate_eflux_linear_coefficients,
    calculate_influx_linear_coefficients,
    detect_baseline_return_idx,
    detect_onset_index,
    detect_peak_index,
    detect_eflux_end_index,
)
from calcium_imaging.viz import create_traces_figure


class ROI:
    """A class representing a single region of interest (ROI) in calcium imaging data.
    
    This class handles the analysis and visualization of calcium imaging data for a single ROI,
    including calculation of influx/eflux rates, amplitude, integral, and tau values.
    
    Attributes:
        coverslip_id (int): The ID of the coverslip this ROI belongs to.
        roi_id (int): The unique identifier for this ROI.
        group_type (str): The type of group this ROI belongs to.
        name (str): A formatted name combining coverslip and ROI IDs.
        title (str): A descriptive title for the ROI.
        time (pd.Series): Time series data for the ROI.
        trace (pd.Series): Fluorescence trace data for the ROI.
        onset_idx (int): Index of the onset of the calcium response.
        peak_idx (int): Index of the peak of the calcium response.
        influx_start_idx (int): Start index for influx calculation.
        influx_end_idx (int): End index for influx calculation.
        eflux_start_idx (int): Start index for eflux calculation.
        eflux_end_idx (int): End index for eflux calculation.
        baseline_return_idx (int): Index where the trace returns to baseline.
    """
    EFLUX_START_INDEX_OFFSET_FROM_PEAK = 5

    def __init__(
            self,
            trace: pd.Series,
            time: pd.Series,
            roi_id: int,
            coverslip_id: int,
            group_type: str,
    ) -> None:
        """Initialize a new ROI instance.
        
        Args:
            trace (pd.Series): The fluorescence trace data for this ROI.
            time (pd.Series): The time series data corresponding to the trace.
            roi_id (int): The unique identifier for this ROI.
            coverslip_id (int): The ID of the coverslip this ROI belongs to.
            group_type (str): The type of group this ROI belongs to.
        """
        self.coverslip_id = coverslip_id
        self.roi_id = roi_id
        self.group_type = group_type
        self.name = f"cs-{self.coverslip_id}_roi-{self.roi_id}"
        self.title = f"ROI {self.roi_id} (Coverslip {self.coverslip_id}, {self.group_type})"
        self.time = time.copy(deep=True).rename(f"time_{self.name}")
        self.trace = trace.copy(deep=True).rename(self.name)
        self.onset_idx = detect_onset_index(self.trace)
        self.peak_idx = detect_peak_index(self.trace)
        self.influx_start_idx = self.onset_idx
        self.influx_end_idx = self.peak_idx
        self.eflux_start_idx = self.peak_idx + self.EFLUX_START_INDEX_OFFSET_FROM_PEAK
        self.eflux_end_idx = detect_eflux_end_index(self.trace)
        self.baseline_return_idx = detect_baseline_return_idx(
            self.trace, self.eflux_start_idx
        )

    def shift_trace(self, periods: int) -> None:
        """Shift the trace and all associated indices by a specified number of periods.
        
        Args:
            periods (int): Number of periods to shift the trace and indices.
        """
        self.time = self.time.shift(periods)
        self.trace = self.trace.shift(periods)
        self.onset_idx = self.onset_idx + periods
        self.peak_idx = self.peak_idx + periods
        self.influx_start_idx = self.influx_start_idx + periods
        self.influx_end_idx = self.influx_end_idx + periods
        self.eflux_start_idx = self.eflux_start_idx + periods
        self.eflux_end_idx = self.eflux_end_idx + periods
        self.baseline_return_idx = min(self.baseline_return_idx + periods, self.trace.index[-1])

    def calculate_influx(self) -> float:
        """Calculate the influx rate of calcium for this ROI.
        
        Returns:
            float: The calculated influx rate.
        """
        return calculate_influx_linear_coefficients(
            trace=self.trace,
            start_idx=self.influx_start_idx,
            end_idx=self.influx_end_idx
        ).slope

    def calculate_eflux(self) -> float:
        """Calculate the eflux rate of calcium for this ROI.
        
        Returns:
            float: The calculated eflux rate.
        """
        return calculate_eflux_linear_coefficients(
            trace=self.trace,
            start_idx=self.eflux_start_idx,
            end_idx=self.eflux_end_idx
        ).slope

    def calculate_amplitude(self) -> float:
        """Calculate the amplitude of the calcium response.
        
        Returns:
            float: The amplitude, calculated as the peak value minus 1.
        """
        return self.trace[self.peak_idx] - 1

    def calculate_integral(self) -> float:
        """Calculate the integral of the trace from onset to baseline return using the trapezoidal rule.
        
        Returns:
            float: The calculated integral of the trace.
            
        Raises:
            ValueError: If baseline_return_idx is not set (equals -999).
        """
        # Get the relevant portions of the trace and time series
        trace_segment = self.trace.loc[self.onset_idx:self.baseline_return_idx + 1]
        time_segment = self.time.loc[self.onset_idx:self.baseline_return_idx + 1]
        
        # Calculate integral using trapezoidal rule
        integral = np.trapz(trace_segment, time_segment)
        return integral

    def calculate_tau(self) -> float:
        """Calculate the time constant (tau) of the calcium response decay.
        
        Tau is calculated as the time between the peak and when the trace reaches
        63.2% of the amplitude decay from peak.
        
        Returns:
            float: The calculated tau value.
        """
        peak_value = self.trace[self.peak_idx]
        target_value = 1 + (peak_value - 1) * 0.368  # 63.2% decay from peak
        
        # Search forward from peak to find where trace crosses target value
        for idx in range(self.peak_idx, len(self.trace)):
            if self.trace.loc[idx] <= target_value:
                return self.time.loc[idx] - self.time.loc[self.peak_idx]
            
        return self.time.loc[self.baseline_return_idx] - self.time.loc[self.peak_idx]  # Return time between peak and baseline return

    def visualize(self, title_prefix: Optional[str] = None) -> None:
        """Create and display a visualization of the ROI trace with key points marked.
        
        Args:
            title_prefix (Optional[str]): Optional prefix to add to the plot title.
        """
        influx_linear_coefficients = calculate_influx_linear_coefficients(
            trace=self.trace,
            start_idx=self.influx_start_idx,
            end_idx=self.influx_end_idx
        )
        eflux_linear_coefficients = calculate_eflux_linear_coefficients(
            trace=self.trace,
            start_idx=self.eflux_start_idx,
            end_idx=self.eflux_end_idx
        )
        create_traces_figure(
            main_trace=self.trace,
            title=self.title if title_prefix is None else f"{title_prefix}\n{self.title}",
            xaxis_title="Frame",
            yaxis_title="Fluorescence relative to background",
            main_trace_peak_index=self.peak_idx,
            main_trace_onset_index=self.onset_idx,
            main_trace_baseline_return_index=self.baseline_return_idx,
            eflux_linear_coefficients=eflux_linear_coefficients,
            influx_linear_coefficients=influx_linear_coefficients
        ).show()

    def set_peak_idx(self, peak_idx: int) -> None:
        """Set a new peak index and update related indices.
        
        Args:
            peak_idx (int): The new peak index to set.
        """
        self.peak_idx = peak_idx
        self.influx_end_idx = self.peak_idx
        self.eflux_start_idx = self.peak_idx + self.EFLUX_START_INDEX_OFFSET_FROM_PEAK
        self.baseline_return_idx = detect_baseline_return_idx(
            self.trace, self.eflux_start_idx
        )

    def set_onset_idx(self, onset_idx: int) -> None:
        """Set a new onset index and update related indices.
        
        Args:
            onset_idx (int): The new onset index to set.
        """
        self.onset_idx = onset_idx
        self.influx_start_idx = self.onset_idx

    def set_baseline_return_idx(self, baseline_return_idx: int) -> None:
        """Set a new baseline return index.
        
        Args:
            baseline_return_idx (int): The new baseline return index to set.
        """
        self.baseline_return_idx = baseline_return_idx

    def __repr__(self) -> str:
        """Return a string representation of the ROI.
        
        Returns:
            str: A string containing the ROI's title.
        """
        return self.title
