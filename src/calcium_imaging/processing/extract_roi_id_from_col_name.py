from typing import Optional

from .constants import ROI_COL_PATTERN


def extract_roi_id_from_col_name(col_name: str) -> Optional[int]:
    """
    Extract the ROI ID from a column name of the form 'ROI <number> (Average)'.

    Parameters
    ----------
    col_name : str
        The column name to inspect.

    Returns
    -------
    Optional[int]
        The integer ROI number if the name matches, otherwise None.
    """
    m = ROI_COL_PATTERN.match(col_name)
    return int(m.group(1)) if m else None
