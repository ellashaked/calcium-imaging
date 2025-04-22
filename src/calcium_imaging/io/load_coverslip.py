from pathlib import Path
from typing import Tuple

import pandas as pd

RawRun = Tuple[str, pd.DataFrame]


def _load_xls_coverslip(xls_path: Path) -> RawRun:
    return xls_path.stem, pd.read_excel(xls_path)


def load_coverslip(path: Path) -> RawRun:
    if path.suffix == ".xls":
        return _load_xls_coverslip(path)
    raise ValueError(f"Unsupported file type '{path.suffix}' for file '{path.resolve()}'")
