from typing import Optional, Tuple, Iterable

import pandas as pd
import plotly.graph_objects as go

from calcium_imaging.analysis import RegressionCoefficients1D


def create_traces_figure(
        main_trace: pd.Series,
        additional_traces: Optional[Iterable[pd.Series]] = None,
        title: Optional[str] = None,
        xaxis_title: Optional[str] = None,
        yaxis_title: Optional[str] = None,
        highlight_index: Optional[float] = None,
        yaxis_range: Optional[Tuple[float, float]] = None,
        eflux_linear_coefficients: Optional[RegressionCoefficients1D] = None,
        influx_linear_coefficients: Optional[RegressionCoefficients1D] = None,
) -> go.Figure:
    # --- base trace ---
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=main_trace.index.values,
            y=main_trace.values,
            mode="lines",
            name=main_trace.name,
            line=dict(color="blue")
        )
    )

    if additional_traces is not None:
        for trace in additional_traces:
            fig.add_trace(
                go.Scatter(
                    x=trace.index.values,
                    y=trace.values,
                    mode="lines",
                    name=trace.name,
                    opacity=0.1,
                    line=dict(color="blue")
                )
            )

    if highlight_index is not None:
        fig.add_trace(
            go.Scatter(
                x=[highlight_index],
                y=[main_trace[highlight_index]],
                mode="markers",
                marker=dict(size=12, color="red", symbol="circle"),
                name="Peak"
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
        yaxis_range=yaxis_range,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )

    return fig
