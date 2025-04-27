import os
from pathlib import Path
from typing import Tuple

import pandas as pd
import xlrd

RawRun = Tuple[str, pd.DataFrame]


def _load_xls(xls_path: Path) -> RawRun:
    wb = xlrd.open_workbook(xls_path, logfile=open(os.devnull, "w"))  # to supress OLE2 inconsistency warning
    df = pd.read_excel(wb, engine="xlrd")
    return xls_path.stem, df


def load_vsi(path: Path) -> RawRun:
    if path.suffix == ".xls":
        return _load_xls(path)
    raise ValueError(f"Unsupported file type '{path.suffix}' for file '{path.resolve()}'")
