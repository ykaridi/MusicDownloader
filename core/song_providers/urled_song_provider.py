from abc import ABC, abstractmethod

from ..song import Song, SongCodec
from ..song_codecs import MP4_AUDIO


class URLedSongProvider(ABC):
    @abstractmethod
    def find_song_by_url(self, url: str, *, codec: SongCodec = MP4_AUDIO) -> Song:
        ...
