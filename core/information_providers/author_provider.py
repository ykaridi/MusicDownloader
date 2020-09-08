from abc import ABC, abstractmethod

from ..musical_author import MusicalArtist


class AuthorProvider(ABC):
    @abstractmethod
    def information(self, author: str) -> MusicalArtist:
        ...
