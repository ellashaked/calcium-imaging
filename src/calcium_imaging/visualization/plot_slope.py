from typing import Optional, Tuple

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from calcium_imaging.data_models import RegressionCoefficients1D


def plot_slope(
        series: pd.Series,
        regression_coefficients: RegressionCoefficients1D,
        fig: Optional[Figure] = None,
        ax: Optional[Axes] = None
) -> Tuple[Figure, Axes]:
    """
    Plot a regression line over the given `series` using the provided coefficients.

    Parameters
    ----------
    series : pd.Series
        The data to visualize alongside the regression line.
    regression_coefficients : RegressionCoefficients1D
        NamedTuple containing `intercept` and `slope` for the line.
    fig : matplotlib.figure.Figure, optional
        Figure to draw on. If None, a new one is created.
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If None, inferred from `fig` or created anew.

    Returns
    -------
    fig, ax : Tuple[Figure, Axes]
        The Figure and Axes used for plotting.
    """
    if ax is None:
        if fig is None:
            fig, ax = plt.subplots()
        else:
            ax = fig.gca()

    # Extract coefficients
    intercept, slope = regression_coefficients

    # Prepare x-values from the series index
    x_vals = series.index.values

    # Compute predicted y-values
    y_vals = intercept + slope * x_vals

    # Plot the regression line
    ax.plot(x_vals, y_vals, linestyle='--', color='black', zorder=3)

    return fig, ax
