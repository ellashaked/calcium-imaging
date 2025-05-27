from typing import List
from typing import Optional, Tuple, Iterable

import pandas as pd
import plotly.graph_objects as go

from calcium_imaging.analysis import RegressionCoefficients1D


def create_traces_figure(
        main_trace: pd.Series,
        main_trace_peak_index: Optional[int] = None,
        main_trace_onset_index: Optional[int] = None,
        additional_traces: Optional[Iterable[pd.Series]] = None,
        additional_traces_peak_indexes: Optional[List[int]] = None,
        additional_traces_onset_indexes: Optional[List[int]] = None,
        title: Optional[str] = None,
        xaxis_title: Optional[str] = None,
        yaxis_title: Optional[str] = None,
        eflux_linear_coefficients: Optional[RegressionCoefficients1D] = None,
        influx_linear_coefficients: Optional[RegressionCoefficients1D] = None,
        yaxis_range: Optional[Tuple[float, float]] = (0.5, 2),
        traces_color: Optional[str] = "blue"
) -> go.Figure:
    # --- base trace ---
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=main_trace.index.values,
            y=main_trace.values,
            mode="lines",
            name=main_trace.name,
            line=dict(color=traces_color),
            legendgroup=main_trace.name,
        )
    )

    if main_trace_peak_index is not None:
        fig.add_trace(
            go.Scatter(
                x=[main_trace_peak_index],
                y=[main_trace[main_trace_peak_index]],
                mode="markers",
                marker=dict(size=8, color="red", symbol="circle"),
                name=f"peak {main_trace.name}",
                opacity=0.5,
                legendgroup=main_trace.name,
                showlegend=False
            )
        )

    if main_trace_onset_index is not None:
        fig.add_trace(
            go.Scatter(
                x=[main_trace_onset_index],
                y=[main_trace[main_trace_onset_index]],
                mode="markers",
                marker=dict(size=8, color="green", symbol="circle"),
                opacity=0.5,
                name=f"onset {main_trace.name}",
                legendgroup=main_trace.name,
                showlegend=False
            )
        )

    if additional_traces is not None:
        for i, trace in enumerate(additional_traces):
            fig.add_trace(
                go.Scatter(
                    x=trace.index.values,
                    y=trace.values,
                    mode="lines",
                    name=trace.name,
                    opacity=0.5,
                    line=dict(color=traces_color),
                    legendgroup=trace.name,
                )
            )
            if additional_traces_peak_indexes is not None:
                fig.add_trace(
                    go.Scatter(
                        x=[additional_traces_peak_indexes[i]],
                        y=[trace[additional_traces_peak_indexes[i]]],
                        mode="markers",
                        marker=dict(size=8, color="red", symbol="circle"),
                        name=f"peak {trace.name}",
                        legendgroup=trace.name,
                        showlegend=False,
                        opacity=0.4,
                    )
                )
            if additional_traces_onset_indexes is not None:
                fig.add_trace(
                    go.Scatter(
                        x=[additional_traces_onset_indexes[i]],
                        y=[trace[additional_traces_onset_indexes[i]]],
                        mode="markers",
                        marker=dict(size=8, color="green", symbol="circle"),
                        name=f"onset {trace.name}",
                        legendgroup=trace.name,
                        showlegend=False,
                        opacity=0.4,
                    )
                )

    if eflux_linear_coefficients is not None:
        x_vals = main_trace.index.values
        y_vals = eflux_linear_coefficients.slope * x_vals + eflux_linear_coefficients.intercept
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="lines",
                line=dict(dash='dash', color='black'),
                name=f"eflux={eflux_linear_coefficients.slope:.4f}"
            )
        )

    if influx_linear_coefficients is not None:
        x_vals = main_trace.index.values
        y_vals = influx_linear_coefficients.slope * x_vals + influx_linear_coefficients.intercept
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode="lines",
                line=dict(dash='dash', color='black'),
                name=f"influx={influx_linear_coefficients.slope:.4f}"
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        yaxis_range=yaxis_range if yaxis_range[1] > main_trace.max() else (yaxis_range[0], main_trace.max() + 0.1),
        template="plotly_white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
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

    return fig
