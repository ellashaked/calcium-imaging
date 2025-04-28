import pandas as pd
from numpy.polynomial.polynomial import polyfit

from .regression_coefficients import RegressionCoefficients1D


def linear_fit(trace: pd.Series, start_idx: int, end_idx: int) -> RegressionCoefficients1D:
    y = trace.loc[start_idx:end_idx]
    x = y.index.to_numpy().astype(float)
    regression_coefficients = RegressionCoefficients1D(*polyfit(x, y, deg=1))
    return regression_coefficients
