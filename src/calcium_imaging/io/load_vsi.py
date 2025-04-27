import os
from pathlib import Path

import pandas as pd
import xlrd


def _load_xls(xls_path: Path) -> pd.DataFrame:
    wb = xlrd.open_workbook(xls_path, logfile=open(os.devnull, "w"))  # to supress OLE2 inconsistency warning
    df = pd.read_excel(wb, engine="xlrd")
    return df


def load_vsi(path: Path) -> pd.DataFrame:
    if path.suffix == ".xls":
        return _load_xls(path)
    raise ValueError(f"Unsupported file type '{path.suffix}' for file '{path.resolve()}'")
