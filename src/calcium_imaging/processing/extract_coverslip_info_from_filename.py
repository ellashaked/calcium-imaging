from typing import NamedTuple

from .constants import COVERSLIP_FILENAME_STEM_PATTERN


# Define the NamedTuple
class CoverslipInfo(NamedTuple):
    coverslip_id: int
    group_type: str


def extract_coverslip_info_from_filename_stem(filename: str) -> CoverslipInfo:
    """
    Extracts coverslip ID and group type from a string of the form
    '<coverslip_id> - <group_type>' and returns a CoverslipInfo tuple.

    Parameters
    ----------
    filename : str
        The filename or label to parse.

    Returns
    -------
    CoverslipInfo
        NamedTuple(coverslip_id, group_type)

    Raises
    ------
    ValueError
        If `name` doesn’t match the expected pattern.
    """
    m = COVERSLIP_FILENAME_STEM_PATTERN.match(filename)
    if not m:
        raise ValueError(
            f"Invalid format {filename!r}; expected '<coverslip_id> - <group_type>'."
        )
    return CoverslipInfo(
        coverslip_id=int(m.group('coverslip_id')),
        group_type=m.group('group_type').strip()
    )
