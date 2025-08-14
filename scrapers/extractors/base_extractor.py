from typing import List, Any

from bs4 import ResultSet


class BaseCellsExtractor:
    """
    Base class for all table cells extractors
    """
    def __init__(self, col_idx: int):
        """
        BaseCellsExtractor constructor
        :param col_idx: the index of the column to extract in the table
        """
        self.col_idx = col_idx

    def extract(self, cells: ResultSet) -> List[Any]:
        raise NotImplementedError("extract method is not implemented")
