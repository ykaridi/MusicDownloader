from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .music_library import MusicLibrary


@dataclass(frozen=True)
class DirectoryStrategy:
    by_album: bool = True
    by_author: bool = False
    by_genre: bool = False


class SongExporter:
    def export_library(self, songs: MusicLibrary, *, path: str = '.', directory_strategy: DirectoryStrategy):
        raise NotImplemented
