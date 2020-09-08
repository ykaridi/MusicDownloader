from dataclasses import dataclass, field
from typing import Optional, Dict, Tuple

from .musical_author import MusicalArtist


@dataclass(frozen=True)
class SongInformation:
    name: str
    album: Optional[str] = None
    track_number: Optional[int] = None
    artists: Optional[Tuple[MusicalArtist, ...]] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    links: Dict[str, str] = field(default_factory=lambda: {})
    additional_information: Optional[str] = None

    def __str__(self):
        song_str = self.name
        if self.year is not None:
            song_str = "%s (%d)" % (song_str, self.year)
        if self.album is not None:
            if self.track_number is not None:
                song_str = "%s @ %s/%d" % (song_str, self.album, self.track_number)
            else:
                song_str = "%s @ %s" % (song_str, self.album)
        if self.artists is not None:
            if len(self.artists) == 1:
                song_str = "%s by %s" % (song_str, self.artists[0])
            else:
                song_str = "%s by %s" % (song_str, "(%s)" % ", ".join(str(artist) for artist in self.artists))
        if self.genre is not None:
            song_str = "%s [%s]" % (song_str, self.genre)
        if self.additional_information is not None:
            song_str = "%s; %s" % (song_str, self.additional_information)

        return song_str
