from abc import ABC, abstractmethod

from ..song_information import SongInformation


class SongInformationProvider(ABC):
    @abstractmethod
    def information(self, song: str) -> SongInformation:
        ...
