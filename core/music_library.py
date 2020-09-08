from collections import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Tuple, Set, Union

from core import Song
from utils.itertools_extended import grouped


@dataclass(frozen=True)
class DirectoryStrategy:
    """
    Represents a directory structuring strategy for saving music libraries
    """
    by_album: bool = True
    by_artist: bool = False


class MusicLibrary(Iterable[Song]):
    """
    Represents a collection of songs.

    Methods
        - append: Add a song
        - extend: Extend an iterable of songs
        - export: Export library to file system
    """

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

    def export(self, path: Union[str, Path] = '.', *, directory_strategy: DirectoryStrategy):
        """Export music library to filesystem"""
        base = Path(path) if isinstance(path, str) else path
        grouped_by_artists = grouped(self.songs, key=lambda song: song.information.artists)
        for artists, songs_by_artist in grouped_by_artists.items():
            artists_base = base / "; ".join(artists) if directory_strategy.by_artist else base
            grouped_by_album = grouped(songs_by_artist, key=lambda song: song.information.album)
            for album, songs_in_album in grouped_by_album.items():
                album_base = base / album if directory_strategy.by_album else artists_base
                for song in songs_in_album:
                    song.save(album_base / song.information.name)
