from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Tuple, Dict, Union

import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from core import SongInformation
from core.song_information import PNGSongImage, JPEGSongImage


@dataclass(frozen=True)
class SpotipyAPI:
    """
    Spotipy API adapter
    """
    client_id: str
    client_secret: str

    @cached_property
    def api(self) -> Spotify:
        return Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret))
