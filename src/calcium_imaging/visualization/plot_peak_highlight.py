import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Optional, Tuple


def plot_peak_highlight(
        series: pd.Series,
        fig: Optional[Figure] = None,
        ax: Optional[Axes] = None
) -> Tuple[Figure, Axes]:
    """
    Highlight the peak of `series` with a red dot.

    Parameters
    ----------
    series : pd.Series
        The data to inspect.
    fig : matplotlib.figure.Figure, optional
        The figure to draw on. If None, a new one is created.
    ax : matplotlib.axes.Axes, optional
        The axes to draw on. If None, inferred from `fig` or created anew.

    Returns
    -------
    fig, ax : the Figure and Axes used.
    """
    # If no axes given, either get from fig or create both
    if ax is None:
        if fig is None:
            fig, ax = plt.subplots()
        else:
            ax = fig.gca()

    # Find and highlight the peak
    peak_idx = series.argmax()
    peak_val = series.iloc[peak_idx]
    ax.scatter(peak_idx, peak_val, color='red', s=100)

    return fig, ax
