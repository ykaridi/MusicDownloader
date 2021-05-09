from abc import ABC, abstractmethod

from .attributed_song import AttributedSong
from .playlist import Playlist


class Scorer(ABC):
    @abstractmethod
    def score(self, song: AttributedSong) -> float:
        ...

    def generate_playlist(self, *songs: AttributedSong, length: int = -1) -> Playlist:
        length = length if length > 0 else len(songs)
        return Playlist(tuple(sorted(songs, key=lambda song: self.score(song), reverse=True)[:length]))
