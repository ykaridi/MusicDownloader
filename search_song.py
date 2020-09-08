from config import SPOTIPY, LAST_FM
from providers import YoutubeProvider


def download_song(name: str):
    track = SPOTIPY.search_track(name)[0]
    yt_url = LAST_FM.get_track_youtube(track.name, track.artists[0])
    return YoutubeProvider().find_song_by_url(yt_url).save(name)
