from dataclasses import dataclass


@dataclass(frozen=True)
class AlterableDataclass:
    """
    Allows altering frozen dataclasses to new instances
    """

    def altered(self, **kwargs):
        """Replaces fields with new values and returns the new instance"""
        params = {field: getattr(self, field) for field in self.__dataclass_fields__}
        for k, v in kwargs.items():
            if k in params:
                params[k] = v

        return self.__class__(**params)
