from dataclasses import dataclass
from pathlib import Path
from typing import Union

from mutagen.mp4 import MP4, MP4Cover

from utils.alterable_dataclass import AlterableDataclass
from .song_codecs import SongCodec
from .song_information import SongInformation, PNGSongImage


@dataclass(frozen=True)
class Song(AlterableDataclass):
    """
    Represents a song.
    Contains actual song (payload and codec), and additional information about it (see SongInformation).
    """

    payload: bytes
    codec: SongCodec
    information: SongInformation

    def save(self, path: Union[str, Path]):
        """Save song to filesystem, including metadata"""
        path = path if isinstance(path, str) else str(path)
        path = "%s.%s" % (path, self.codec.extension)
        with open(path, 'wb') as file:
            file.write(self.payload)

        tags = {
            '\xa9nam': self.information.name,
            '\xa9alb': self.information.album,
            '\xa9ART': "; ".join(self.information.artists) if self.information.artists is not None else None,
            'trkn': (self.information.track_number, ) if self.information.album is not None else None,
            '\xa9day': str(self.information.year),
            '\xa9gen': self.information.genre,
            'covr': (MP4Cover(self.information.cover_image.payload,
                              imageformat=MP4Cover.FORMAT_PNG if isinstance(self.information.cover_image, PNGSongImage)
                             else MP4Cover.FORMAT_JPEG), ) if self.information.cover_image is not None else None
        }

        file = MP4(path)
        for k, v in tags.items():
            if v is not None:
                file[k] = v

        file.save()
