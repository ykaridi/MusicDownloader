from abc import ABC, abstractmethod

from ..song import Song, SongCodec
from ..song_codecs import MP4_AUDIO


class NamedSongProvider(ABC):
    @abstractmethod
    def find_song_by_name(self, name: str, *, codec: SongCodec = MP4_AUDIO) -> Song:
        ...
