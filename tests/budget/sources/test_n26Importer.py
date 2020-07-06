from datetime import date
from unittest import TestCase

from pandas import DataFrame

from budget.sources.n26 import N26Importer


def _generate_record(amount: str) -> dict:
    return {
        "Date": "05.11.2019",
        "Payee": "Terry Pratchett",
        "Account number": "DExxx",
        "Transaction type": "MasterCard Payment",
        "Payment reference": "",
        "Category": "Outgoing Transfer",
        "Amount (EUR)": amount,
        "Amount (Foreign Currency)": amount,
        "Type Foreign Currency": "EUR",
        "Exchange Rate": "1.0",
    }


class TestN26Importer(TestCase):
    subject = N26Importer()

    def test_import(self):
        amount = "-12.45"
        records_df = DataFrame([_generate_record(amount)])
        actual = self.subject.parse(records_df)

        assert actual[0].amount == amount
        assert actual[0].recorded_at == date.fromisoformat("2019-11-05")
