Music Downloader
================

Provides an easy API to download music with,
```python
from downloaders import download_song, download_album

download_song('Counting Stars', artist='One Republic')
download_album('My Head is an Animal', artist='Of Monsters and Men')
```

Provides also more advanced usage, supports base paths, suffixes 
 and audio flavours to be used as follows,
 ```python
from downloaders import download_song, download_album

BASE = 'Music'
FLAVOUR = 'Karaoke'
SUFFIX = 'Karaoke Party 1/1/1970'

download_song('Counting Stars', artist='One Republic')
download_album('My Head is an Animal', artist='Of Monsters and Men')
```

## Setup
All that is needed in the setup is to configure Spotify API, 
and optionally Last.FM API. 
Configuration is located at config/config.py (omitted from repository) and should contain
```python
from config.last_fm import LastFM
from config.spotipy import SpotipyAPI

SPOTIPY = SpotipyAPI(..., ...)
LAST_FM = LastFM(..., ...)
```