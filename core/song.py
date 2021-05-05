from dataclasses import dataclass
from pathlib import Path
from typing import Union

from mutagen.mp4 import MP4, MP4Cover

from utils.alterable_dataclass import AlterableDataclass
from .song_codecs import SongCodec, CODECS
from .song_information import SongInformation, PNGSongImage, JPEGSongImage

MP4_NAME            = '\xa9nam'
MP4_ALBUM           = '\xa9alb'
MP4_ARTISTS         = '\xa9ART'
MP4_TRACK_NUMBER    = 'trkn'
MP4_YEAR            = '\xa9day'
MP4_GENRE           = '\xa9gen'
MP4_COVER_IMAGE     = 'covr'
MP4_SYNOPSIS        = 'ldes'
MP4_DESCRIPTION     = '\xa9des'
MP4_COMMENTS        = '\xa9cmt'


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
            MP4_NAME: self.information.name,
            MP4_ALBUM: self.information.album,
            MP4_ARTISTS: "; ".join(self.information.artists) if self.information.artists is not None else None,
            MP4_TRACK_NUMBER: (self.information.track_number, ) if self.information.album is not None else None,
            MP4_YEAR: str(self.information.year),
            MP4_GENRE: self.information.genre,
            MP4_COVER_IMAGE: (MP4Cover(self.information.cover_image.payload,
                                       imageformat=MP4Cover.FORMAT_PNG
                                       if isinstance(self.information.cover_image, PNGSongImage)
                                       else MP4Cover.FORMAT_JPEG), ) if self.information.cover_image is not None else None,
            MP4_SYNOPSIS: self.information.additional_information,
            MP4_COMMENTS: self.information.additional_information
        }

        file = MP4(path)
        for k, v in tags.items():
            if v is not None:
                file[k] = v

        file.save()

    @staticmethod
    def load(path: Union[str, Path]):
        path = Path(path) if isinstance(path, str) else path
        codec = next((codec for codec in CODECS if codec.extension == path.suffix[1:]), None)
        if not codec:
            raise ValueError("Invalid file")

        file = MP4(path)
        with open(path, 'rb') as f:
            payload = f.read()

        unlist = lambda o: o[0] if o else None

        _artists = unlist(file.get(MP4_ARTISTS, None))
        _cover = unlist(file.get(MP4_COVER_IMAGE, None))
        cover = (PNGSongImage(bytes(_cover)) if _cover.imageformat == MP4Cover.FORMAT_PNG
                 else JPEGSongImage(bytes(_cover))) if _cover else None

        information = SongInformation(
            name=unlist(file.get(MP4_NAME, path.name.rsplit('.', 2)[0])),
            album=unlist(file.get(MP4_ALBUM, None)),
            track_number=unlist(file.get(MP4_TRACK_NUMBER, None)),
            artists=tuple(_artists.split('; ')) if _artists else None,
            cover_image=cover,
            year=unlist(file.get(MP4_YEAR, None)),
            genre=unlist(file.get(MP4_GENRE, None)),
            links={},
            additional_information=unlist(file.get(MP4_SYNOPSIS))
        )

        return Song(payload, codec, information)
