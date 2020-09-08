from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Tuple

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from core import SongInformation


@dataclass(frozen=True)
class SpotipyAPI:
    client_id: str
    client_secret: str

    def _search(self, query_type: str, limit: int = 10, **query: Optional[str]):
        return self.api.search(" ".join("%s:%s" % (k, v) for k, v in query.items() if v is not None), type=query_type,
                               limit=limit)[query_type + "s"]['items']

    def search_track(self, track: Optional[str] = None, artist: Optional[str] = None) -> Tuple[SongInformation, ...]:
        def _inner():
            for result in self._search(query_type="track", track=track, artist=artist):
                name: str = result['name']
                album: str = result['album']['name']
                year: int = int(result['album']['release_date'].split("-")[0])
                track_number: int = int(result['track_number'])
                artists = tuple(art['name'] for art in result['artists'])
                links = result['external_urls']

                yield SongInformation(name, album, track_number, artists, year, links=links)

        return tuple(_inner())

    def search_album(self, album: Optional[str] = None, artist: Optional[str] = None):
        return tuple(self._search(query_type="album", album=album, artist=artist))

    @cached_property
    def api(self) -> Spotify:
        return Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret))
