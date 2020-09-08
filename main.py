from pathlib import Path

from downloaders import download_album


BASE = Path("Music")
if not BASE.exists():
    BASE.mkdir()
FLAVOUR = "Audio"
# SUFFIX = FLAVOUR


if __name__ == '__main__':
    download_album("A Head Full of Dreams", artist="Coldplay")
