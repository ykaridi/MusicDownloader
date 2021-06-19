from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from .attributed_song import AttributedSong
from .playlist import Playlist


class Scorer(ABC):
    @property
    def reverse_score(self) -> bool:
        return True

    @abstractmethod
    def score(self, song: AttributedSong) -> float:
        ...

    def generate_playlist(self, *songs: AttributedSong, length: int = -1) -> Playlist:
        length = length if length > 0 else len(songs)
        return Playlist(tuple(sorted(songs, key=lambda song: self.score(song),
                                     reverse=self.reverse_score)[:length]))


@dataclass(frozen=True)
class AveragingScorer(Scorer):
    attribute_weights: Dict[str, float]
    reverse: bool = True

    @property
    def reverse_score(self) -> bool:
        return self.reverse

    def score(self, song: AttributedSong) -> float:
        return sum(song.attributes[attr] * weight for attr, weight in self.attribute_weights.items())
