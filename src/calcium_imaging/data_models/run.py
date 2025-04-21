import pandas as pd


class Run:
    """One plate"""

    def __init__(self, name: str, df: pd.DataFrame) -> None:
        """Reads an Excel path and turns it into a run object"""
        self.name = name
        self.df = df
        self.id = self.name.split("-")[0].strip()  # TODO regex
        self.condition_type = self.name.split("-")[-1].strip()  # TODO regex

    def __repr__(self) -> str:
        return str(self.name)
