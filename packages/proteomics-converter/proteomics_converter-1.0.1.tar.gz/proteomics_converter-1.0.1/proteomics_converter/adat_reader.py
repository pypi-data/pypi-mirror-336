from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, TextIO

import numpy as np
from somadata import read_adat, Adat

from proteomics_converter.adat_func import create_dfs_from_multiple_adat


class AdatReader(ABC):
    """ABC for reading multiple proteomics input"""

    @abstractmethod
    def adat(self) -> Adat:
        pass


class FileAdatReader(AdatReader):
    """(v1) Read an adat file"""

    def __init__(self, file: Union[str, TextIO]) -> None:
        self.file = file

    def adat(self) -> Adat:
        adat = read_adat(self.file)
        return adat


class MultiFileAdatReader(AdatReader):
    """(v2) Given multiple adat files, return one big adat"""

    def __init__(self, files: list[Union[str, TextIO]]) -> None:
        self.files = files

    def adat(self) -> Adat:
        sample_df, somamer_df, count_df = create_dfs_from_multiple_adat([read_adat(adat) for adat in self.files])
        sample_dict = sample_df.reset_index(drop=True).to_dict(orient='list')
        somamer_dict = somamer_df.reset_index(drop=True).to_dict(orient='list')
        count_matrix = np.asmatrix(count_df)

        return Adat.from_features(
            rfu_matrix=count_matrix,
            row_metadata=sample_dict,
            column_metadata=somamer_dict,
            header_metadata={},
        )


class FolderAdatReader(AdatReader):
    """(v2) Given a cassini-app output dir, return one big adat"""

    def __init__(self, path: Union[Path, str]) -> None:
        self.path = path

    def adat(self) -> Adat:
        """TODO Extract list of adat files from dir, then concatenate them into a big adat"""
        pass
