from pathlib import Path


class Run:
    """One plate"""

    def __init__(self, xls_path: Path) -> None:
        """Reads an Excel path and turns it into a run object"""
        self.xls_path = xls_path
        self.condition = 5
