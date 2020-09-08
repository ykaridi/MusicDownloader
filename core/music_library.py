from collections import Iterable
from typing import Iterator, Tuple, Set

from core import Song
from core.exporter import DirectoryStrategy


class MusicLibrary(Iterable[Song]):
    def __init__(self, *songs: Song):
        self._songs: Set[Song] = set(songs)

    @property
    def songs(self) -> Tuple[Song]:
        return tuple(self._songs)

    def append(self, song: Song):
        self._songs.add(song)

    def extend(self, songs: Iterable[Song]):
        self._songs.update(songs)

    def __iter__(self) -> Iterator[Song]:
        return iter(self._songs)

    def export(self, path: str = '.', *, directory_strategy: DirectoryStrategy):
        raise NotImplemented
