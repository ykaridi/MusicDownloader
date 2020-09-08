from core import SongInformationProvider, SongInformation


class LastFMProvider(SongInformationProvider):
    def information(self, song: str) -> SongInformation:
        pass