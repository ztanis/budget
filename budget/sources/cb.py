from datetime import datetime, timezone

import pandas as pd

from budget.sources.base import BaseImporter
from budget.models.record import Record
from typing import Dict, Any, List
from pandas import DataFrame

class CBImporter(BaseImporter):
    columns = [
        'booking_date',
        'processed_at',
        'operation',
        'name',
        'amount',
        'currency',
        'target',
        'target_bank',
        'account',
        'category'
    ]
    
    def parse(self, records_df: DataFrame) -> List[Record]:
        transformed_records_df = self._transform(records_df)
        records = self._to_dicts(transformed_records_df)

        return [self._to_record(row) for row in records]

    def read(self, filename: str) -> DataFrame:
        return pd.read_csv(filename, sep=';', decimal=',', names=self.columns, header=0, index_col=False)

    @staticmethod
    def _transform(records_df: DataFrame) -> DataFrame:
        now = datetime.now()

        records_df['recorded_at'] = records_df['booking_date'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y'))
        records_df['name'] = records_df['name'].apply(lambda x: x[:255])
        records_df['created_at'] = now
        records_df['updated_at'] = now
        return records_df

    @staticmethod
    def _to_dicts(records_df: DataFrame):
        return records_df.T.to_dict().values()

    @staticmethod
    def _to_record(record: Dict[str, Any]) -> Record:
        return Record(
            name=record['name'],
            category_id=None,
            account=record['account'],
            amount=record['amount'],
            comment="",
            recorded_at=record['recorded_at'],
            created_at=record['created_at'],
            updated_at=record['updated_at']
        )
