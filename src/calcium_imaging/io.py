from pathlib import Path
from typing import Tuple

import pandas as pd


RawRun = Tuple[str, pd.DataFrame]


def load_xls_run(xls_path: Path) -> RawRun:
    return xls_path.stem, pd.read_excel(xls_path)


def load_run(path: Path) -> RawRun:
    if path.suffix == ".xls":
        return load_xls_run(path)
    raise ValueError(f"Unsupported file type '{path.suffix}' for file '{path.resolve()}'")
