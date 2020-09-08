from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MusicalArtist:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    alias: Optional[str] = None

    def __post_init__(self):
        if all(field is None for field in (self.first_name, self.last_name, self.alias)):
            raise ValueError("Must contain at least one non-empty field")

    def __str__(self) -> str:
        name_part: Optional[str] = None
        if self.first_name or self.last_name:
            name_part = " ".join((self.first_name, self.last_name))
        elif self.alias is not None:
            return self.alias

        alias_part: Optional[str] = "AKA %s" % self.alias if self.alias is not None else None

        return " ".join(filter(lambda field: field is not None, (name_part, alias_part)))
