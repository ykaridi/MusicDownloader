from abc import ABC, abstractmethod
from typing import Tuple

from ..song_information import SongInformation


class AlbumInformationProvider(ABC):
    """
    Information provider for albums returns album name and song information for songs in it
    """

    @abstractmethod
    def search_album(self, album: str, artist: str = None) -> Tuple[str, Tuple[SongInformation, ...]]:
        """
        Searches for an album
        :param album:
        :param artist:
        :return: album name, information of all songs in the album
        """
        ...
