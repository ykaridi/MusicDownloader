from dataclasses import dataclass

from .song_codecs import SongCodec
from .song_information import SongInformation


@dataclass(frozen=True)
class Song:
    payload: bytes
    codec: SongCodec
    information: SongInformation

    def save(self, path: str):
        with open("%s.%s" % (path, self.codec.extension), 'wb') as file:
            file.write(self.payload)
