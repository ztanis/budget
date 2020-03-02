from typing import List

from pandas import DataFrame

from budget.context import db
from budget.models.record import Record
from budget.models.category import Category
import logging


class BaseImporter:
    def read(self, filename: str):
        pass

    def parse(self, record_df: DataFrame):
        pass

    @classmethod
    def save(cls, records: List[Record]):
        unique = cls._filter_exists(records)
        logging.info(f"Saving unique {len(unique)} records out of {len(records)} in total")
        for record in unique:
            print(record)
            db.session.add(record)
        db.session.commit()
        logging.info(f"Saved!")

    @classmethod
    def _filter_exists(cls, records):
        return [r for r in records if not cls._is_exists(r)]

    @classmethod
    def _is_exists(cls, record: Record):
        return db.session.query(
            Record.query.filter(
                Record.name == record.name,
                Record.amount == record.amount,
                Record.recorded_at == record.recorded_at,
            ).exists()
        ).scalar()
