from datetime import datetime
from typing import List

import dateutil
import pandas as pd
from pandas import DataFrame, Series

from budget.models.record import Record
from budget.sources.base import BaseImporter


class N26Importer(BaseImporter):
    columns = [
        "Date",
        "Payee",
        "Account number",
        "Transaction type",
        "Payment reference",
        "Category",
        "Amount (EUR)",
        "Amount (Foreign Currency)",
        "Type Foreign Currency",
        "Exchange Rate",
    ]

    def parse(self, records_df: DataFrame) -> List[Record]:
        return list(
            records_df.pipe(self._transform)
            .apply(self._to_record, axis="columns")
            .values
        )

    def read(self, filename: str) -> DataFrame:
        return pd.read_csv(
            filename,
            sep=",",
            decimal=".",
            names=self.columns,
            header=0,
            index_col=False,
        )

    @staticmethod
    def _transform(records_df: DataFrame) -> DataFrame:
        now = datetime.now()
        return records_df.assign(
            recorded_at=records_df["Date"].apply(dateutil.parser.parse),
            name=records_df["Payee"].apply(lambda x: x[:255]),
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _to_record(row: Series) -> Record:
        return Record(
            name=row["name"],
            category_id=None,
            account=row["Account number"],
            amount=row["Amount (EUR)"],
            comment="",
            recorded_at=row["recorded_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
