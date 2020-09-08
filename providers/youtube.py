from io import BytesIO

from core import URLedSongProvider, Song, SongInformation
from core.song_codecs import SongCodec, MP4_AUDIO
from utils import patch_pytube

from pytube import YouTube


patch_pytube()


class YoutubeProvider(URLedSongProvider):
    def find_song_by_url(self, url: str, *, codec: SongCodec = MP4_AUDIO) -> Song:
        yt = YouTube(url)
        bytes_io = BytesIO()
        yt.streams.filter(mime_type=codec.mime_type).first().stream_to_buffer(bytes_io)
        bytes_io.seek(0)
        return Song(bytes_io.read(), codec, SongInformation(yt.title))
