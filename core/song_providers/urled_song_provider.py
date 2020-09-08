from abc import ABC, abstractmethod

from ..song import Song, SongCodec
from ..song_codecs import MP4_AUDIO


class URLedSongProvider(ABC):
    """
    Song provider, returns a song object given a url holding it
    """

    @abstractmethod
    def find_song_by_url(self, url: str, *, codec: SongCodec = MP4_AUDIO) -> Song:
        """
        Generates a song object given the song's name
        :param url: URL song is held in
        :param codec: Codec to encode song in
        :return:
        """
        ...
