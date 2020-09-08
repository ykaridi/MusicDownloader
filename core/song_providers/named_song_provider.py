from abc import ABC, abstractmethod

from ..song import Song, SongCodec
from ..song_codecs import MP4_AUDIO


class NamedSongProvider(ABC):
    """
    Song provider, returns a song object given a song name query
    """

    @abstractmethod
    def find_song_by_name(self, name: str, *, codec: SongCodec = MP4_AUDIO) -> Song:
        """
        Generates a song object given the song's name
        :param name: Song name (might contain also additional information like artist)
        :param codec: Codec to encode song in
        :return:
        """
        ...
