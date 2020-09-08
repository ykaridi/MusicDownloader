from abc import ABC, abstractmethod

from ..song_information import SongInformation


class SongInformationProvider(ABC):
    """
    Information provider for songs, returns song information
    """
    @abstractmethod
    def search_song(self, song: str, album: str = None, artist: str = None) -> SongInformation:
        """
        Searches for a song
        :param song:
        :param album:
        :param artist:
        :return: Song information
        """
        ...
