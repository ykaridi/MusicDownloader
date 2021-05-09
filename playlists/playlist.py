import time
from dataclasses import dataclass
from typing import Tuple
import vlc

from core import Song
from utils.mp4_bytes_player import media_from_mp4_bytes


@dataclass(frozen=True)
class Playlist:
    songs: Tuple[Song, ...]

    def play(self, listen_block: bool = False) -> vlc.MediaListPlayer:
        player = media_from_mp4_bytes(*(song.payload for song in self.songs))
        player.play()

        if listen_block:
            while player.get_state() != 6:
                time.sleep(1)

        return player
