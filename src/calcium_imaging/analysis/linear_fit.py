import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import polyfit

from calcium_imaging.data_models import RegressionCoefficients1D


def linear_fit(series: pd.Series, start_idx: int, end_idx: int) -> RegressionCoefficients1D:
    y = series.iloc[start_idx:end_idx]
    x = np.arange(len(y))
    regression_coefficients = RegressionCoefficients1D(*polyfit(x, y, deg=1))
    return regression_coefficients
