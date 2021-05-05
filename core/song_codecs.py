from dataclasses import dataclass


@dataclass(frozen=True)
class SongCodec:
    """
    Represents a sound codec
    """
    mime_type: str
    extension: str


MP4 = SongCodec("video/mp4", 'mp4')
MP4_AUDIO = SongCodec("audio/mp4", 'm4a')

CODECS = [MP4, MP4_AUDIO]
