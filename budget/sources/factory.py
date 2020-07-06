from budget.sources.base import BaseImporter
from budget.sources.cb import CBImporter
from budget.sources.n26 import N26Importer


class Factory:
    _importers = {
        "cb": CBImporter(),
        "n26": N26Importer()
    }

    @classmethod
    def get(cls, name: str) -> BaseImporter:
        return cls._importers[name]
