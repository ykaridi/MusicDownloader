from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

from core import Song


@dataclass(frozen=True)
class AttributedSong(Song):
    attributes: Dict[str, float]

    @staticmethod
    def from_song(song: Song) -> AttributedSong:
        lines = song.information.additional_information.split("\n")
        split_lines = (line.split(" ") for line in lines)
        return AttributedSong(**vars(song), attributes={k: float(v) for k, v in split_lines})
