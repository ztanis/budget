import datetime

import pandas as pd
import pytz

from budget.context import db
from budget.importers.base import BaseImporter
from budget.models.record import Record


class CBImporter(BaseImporter):
    columns = ['booking_date', 'processed_at', 'payment_type', 'name', 'amount', 'currency', 'target', 'target_bank', 'account', 'category']
    timezone = pytz.timezone('UTC')
    def parse(self, filename):
        print(filename)
        df = pd.read_csv(filename, sep = ';', decimal=',', names = self.columns, header=0)
        df['recorded_at'] = df['booking_date'].apply(lambda x:
             datetime.datetime.strptime(x, '%d.%m.%Y')
        )

        df['name'] = df['name'].apply(lambda x: x[:255])
        print(df)
        #print(df)
        rows = df.T.to_dict().values()
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        for row in rows:
            print(row)
            record = Record(
                name = row['name'],
                category_id = None,
                account = row['account'],
                amount = row['amount'],
                comment = "",
                recorded_at = row['recorded_at'],
                created_at = now,
                updated_at = now
            )
            exists = db.session.query(
                Record.query.filter(
                    Record.name == record.name,
                    Record.amount == record.amount,
                    Record.recorded_at == record.recorded_at,
                ).exists()
            ).scalar()

        #print(row)
            if not exists:
                db.session.add(record)
        print("commit")
        db.session.commit()
        print("commited")

