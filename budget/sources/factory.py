from budget.sources.base import BaseImporter
from budget.sources.cb import CBImporter


class Factory:
    _importers = {
        'cb': CBImporter()
    }

    @classmethod
    def get(cls, name: str) -> BaseImporter:
        return cls._importers[name]
