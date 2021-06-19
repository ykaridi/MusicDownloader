from dataclasses import dataclass, field
from typing import Optional, Dict, Tuple, Union

from utils.alterable_dataclass import AlterableDataclass


@dataclass(frozen=True)
class PNGSongImage:
    """
    Represents a PNG image,
    used internally for cover images
    """

    payload: bytes = field(repr=False)


@dataclass(frozen=True)
class JPEGSongImage:
    """
    Represents a JPEG image,
    used internally for cover images
    """

    payload: bytes = field(repr=False)


@dataclass(frozen=True)
class SongInformation(AlterableDataclass):
    """
    Holds information of a given song, contains
    - name
    - album name
    - track number, total tracks
    - artists
    - cover image
    - release year
    - genre
    - external links
    - some additional information about the song
    """

    name: str
    album: Optional[str] = None
    track_number: Optional[Tuple[int, int]] = None
    artists: Optional[Tuple[str, ...]] = None
    cover_image: Optional[Union[PNGSongImage, JPEGSongImage]] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    links: Dict[str, str] = field(default_factory=lambda: {})
    additional_information: Optional[str] = None

    def __str__(self):
        song_str = self.name
        if self.year is not None:
            song_str = f"{song_str} ({self.year})"
        if self.album is not None:
            if self.track_number is not None:
                song_str = f"{song_str} @ {self.album}/{self.track_number[0]}"
            else:
                song_str = f"{song_str} @ {self.album}"
        if self.artists is not None:
            song_str = f"{song_str} by {', '.join(self.artists)}"
        if self.genre is not None:
            song_str = f"{song_str} [{self.genre}]"
        if self.additional_information is not None:
            song_str = f"{song_str}; {self.additional_information}"

        return song_str
