from unittest import TestCase
from budget.sources.cb import CBImporter
import pytest
from pandas import DataFrame
from datetime import date

# TODO share this data using pytest datafiles https://docs.pytest.org/en/latest/fixture.html#sharing-test-data
def _generate_record(amount: str, name: str):
    return {
        'booking_date': '05.11.2019',
        'processed_at': '05.11.2019',
        'payment_type': 'Lastschrift',
        'name': name,
        'amount' : amount,
        'currency': 'EUR',
        'target': '123',
        'target_bank': '456',
        'account': 'DExxx',
        'category': 'Unkategorisierte Ausgaben',
    }


class TestCBImporter(TestCase):
    subject = CBImporter()

    def test_import(self):
        records_df = DataFrame([_generate_record('-12.45', 'Supermarket ocean wave')])
        actual = self.subject.parse(records_df)

        assert(actual[0].name == 'Supermarket ocean wave')
        assert(actual[0].amount == '-12.45')
        assert(actual[0].recorded_at == date.fromisoformat('2019-11-05'))
