from pathlib import Path
from downloaders import download_album


BASE = Path("Music")
FLAVOUR = "Acoustic"
SUFFIX = FLAVOUR if (FLAVOUR and FLAVOUR.lower() != 'audio') else None


if __name__ == '__main__':
    if not BASE.exists():
        BASE.mkdir()
    
    download_album("A Head Full of Dreams", artist="Coldplay")
