from io import BytesIO

from youtube_search import YoutubeSearch

from core import URLedSongProvider, Song, SongInformation, NamedSongProvider
from core.song_codecs import SongCodec, MP4_AUDIO
from utils import patch_pytube

from pytube import YouTube


patch_pytube()


class YoutubeProvider(URLedSongProvider, NamedSongProvider):
    """
    Song providers from Youtube
    """

    def find_song_by_url(self, url: str, *, codec: SongCodec = MP4_AUDIO) -> Song:
        yt = YouTube(url)
        bytes_io = BytesIO()
        # TODO: Try download best quality?
        yt.streams.filter(mime_type=codec.mime_type).first().stream_to_buffer(bytes_io)
        bytes_io.seek(0)
        return Song(bytes_io.read(), codec, SongInformation(yt.title))

    def find_song_by_name(self, name: str, *, codec: SongCodec = MP4_AUDIO) -> Song:
        search = YoutubeSearch(name).videos[0]
        return self.find_song_by_url("https://youtube.com/watch?v=%s" % search['id'])
