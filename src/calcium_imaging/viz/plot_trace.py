from typing import Optional, Tuple

import pandas as pd
import plotly.graph_objects as go


def plot_trace(
        trace: pd.Series,
        title: Optional[str] = None,
        xaxis_title: Optional[str] = None,
        yaxis_title: Optional[str] = None,
        highlight_index: Optional[float] = None,
        yaxis_range: Optional[Tuple[float, float]] = None
) -> None:
    # --- base trace ---
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=trace.index.values,
            y=trace.values,
            mode="lines",
            name="Trace"
        )
    )

    if highlight_index is not None:
        fig.add_trace(
            go.Scatter(
                x=[highlight_index],
                y=[trace[highlight_index]],
                mode="markers",
                marker=dict(size=12, color="red", symbol="circle"),
                name="Peak"
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

    fig.show()
