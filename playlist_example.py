from pathlib import Path

from core import Song
from playlists import AttributedSong, AveragingScorer


if __name__ == '__main__':
    song_files = Path('Music').glob('**/*.m4a')
    songs = map(Song.load, song_files)
    attributed_songs = list(map(AttributedSong.from_song, songs))

    attrs = {}
    while attr := input("Attribute: "):
        weight = float(input("Weight: ") or 1)
        attrs[attr] = weight

    scorer = AveragingScorer(attrs)
    playlist = scorer.generate_playlist(*attributed_songs)
    player = playlist.play()

    while (c := input("> ").lower()) not in ('s', 'stop'):
        if c in ('n', 'next'):
            player.next()
        elif c in ('p', 'pause'):
            player.set_pause(player.is_playing())
        elif c in ('r', 'resume'):
            player.play()
        elif c in ('b', 'back'):
            player.previous()

    player.stop()
