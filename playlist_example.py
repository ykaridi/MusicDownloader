from pathlib import Path

from core import Song
from playlists import Scorer, AttributedSong


class ExampleScorer(Scorer):
    def score(self, song: AttributedSong) -> float:
        return song.attributes['liveness']


if __name__ == '__main__':
    song_files = Path('Music/').glob('**/*.m4a')
    songs = map(Song.load, song_files)
    attributed_songs = list(map(AttributedSong.from_song, songs))

    scorer = ExampleScorer()
    playlist = scorer.generate_playlist(*attributed_songs)
    player = playlist.play()

    while (c := input("> ")) not in ('s', 'stop'):
        if c in ('n', 'next'):
            player.next()
