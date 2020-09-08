from dataclasses import dataclass
from functools import cached_property
from typing import Optional

import requests
import re

from pylast import LastFMNetwork


@dataclass(frozen=True)
class LastFM:
    api_key: str
    api_secret: str

    def get_track_youtube(self, track_name: str, author_name: str) -> Optional[str]:
        url = self.api.get_track(author_name, track_name).get_url()
        result = requests.get(url).text
        re_result = re.search(r'''data-youtube-url="(https://www.youtube.com/.*)"''', result)
        return re_result.group(1) if re_result is not None else None

    @cached_property
    def api(self):
        return LastFMNetwork(api_key=self.api_key, api_secret=self.api_secret)
