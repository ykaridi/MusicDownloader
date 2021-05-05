import traceback
from pathlib import Path
from sys import stderr
from typing import Callable, Union

from config import LAST_FM
from core import SongInformation, Song
from providers import YoutubeProvider
from providers.spotify import SpotifyProvider
from utils import ScopeResolver

spotify_provider = SpotifyProvider()
yt_provider = YoutubeProvider()


def find_on_lastfm(track_information: SongInformation) -> Song:
    """Searches for track on LastFM and then downloads from Youtube link provided"""
    yt_url = LAST_FM.get_track_youtube(track_information.name, track_information.artists[0])
    if yt_url is None:
        raise ValueError("Song not found on LastFM")
    return YoutubeProvider().find_song_by_url(yt_url)


@ScopeResolver('flavour')
def find_on_youtube(track_information: SongInformation, *, flavour: str = "Audio") -> Song:
    """
    Searches for song on Youtube, query looks like song_name - song_author (flavour)
    :param track_information:
    :param flavour: [Resolved implicitly by scope]
    :return:
    """
    return YoutubeProvider().find_song_by_name("%s - %s %s"
                                               % (track_information.name, track_information.artists[0], flavour))


@ScopeResolver('base', 'suffix', 'suffix_song', 'track_resolver', 'retries')
def download_song(name: str, *, album: str = None, artist: str = None, base: Union[str, Path] = ".", suffix: str = None,
                  suffix_song: bool = False, track_resolver: Callable[[SongInformation], Song] = find_on_youtube, retries: int = 3):
    """
    Downloads song given song name and (optional) album name
    :param name: Song name
    :param album: Album name
    :param artist: Artist name
    :param base: Base path to save song to [Resolved implicitly by scope]
    :param suffix: Suffix to append to filename [Resolved implicitly by scope]
    :param suffix_song: Append suffix to song name as well
    :param track_resolver: Resolver for downloading actual audio [Resolved implicitly by scope]
    :param retries: Number of attempts to download song [Resolved implicitly by scope]
    """
    base = base if isinstance(base, Path) else Path(base)
    track_information = spotify_provider.search_song(name, album, artist)
    for idx in range(retries):
        try:
            print("Downloading %s (%d / %d tries)" % (track_information.name, (idx + 1), retries))
            if suffix_song:
                track_information = track_information.altered(name="%s (%s)" % (track_information.name, suffix))

            track_resolver(track_information).altered(information=track_information).save(
                base / (track_information.name + ("" if suffix is None else " %s" % suffix))
            )
            return
        except:  # noqa
            traceback.print_exc()
            print("\tFailed downloading %s" % track_information.name, file=stderr)


@ScopeResolver('base', 'suffix', 'suffix_album', 'suffix_song', 'track_resolver', 'retries')
def download_album(name: str, *, artist: str = None, base: Union[str, Path] = ".", suffix: str = None,
                   suffix_album: bool = True, suffix_song: bool = False,
                   track_resolver: Callable[[SongInformation], Song] = find_on_youtube, retries: int = 3):
    """
    Downloads song given song name and (optional) album name
    :param name: Song name
    :param artist: Artist name
    :param base: Base path to save song to [Resolved implicitly by scope]
    :param suffix: Suffix to append to filename [Resolved implicitly by scope]
    :param suffix_album: Append suffix to album as well
    :param suffix_song: Append suffix to song name as well
    :param track_resolver: Resolver for downloading actual audio [Resolved implicitly by scope]
    :param retries: Number of attempts to download song [Resolved implicitly by scope]
    """
    album_name, tracks = spotify_provider.search_album(name, artist)
    print("Downling %s" % album_name)
    base = base if isinstance(base, Path) else Path(base)
    base /= album_name + ("" if suffix is None else " %s" % suffix)
    if not base.exists():
        base.mkdir()
    for track_information in tracks:
        for idx in range(retries):
            try:
                print("\tDownloading %s (%d / %d tries)" % (track_information.name, (idx + 1), retries))
                if suffix_song:
                    track_information = track_information.altered(name="%s (%s)" % (track_information.name, suffix))
                filename = track_information.name.replace('/', ' ').replace('.', ' ')

                if track_information.track_number:
                    filename = "%02d %s" % (track_information.track_number[0], filename)
                if suffix_album:
                    track_information = track_information.altered(album="%s (%s)" % (track_information.album, suffix))

                track_resolver(track_information).altered(information=track_information).\
                    save(base / filename)
                break
            except:  # noqa
                traceback.print_exc()
                print("> Failed downloading %s" % track_information.name, file=stderr)
