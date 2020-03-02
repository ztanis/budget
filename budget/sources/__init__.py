from budget.context import db
from budget.sources.cb import CBImporter
from budget.models.statement import Statement, StatementStatus
from budget.models.statement import file_path
from budget.sources.factory import Factory


def import_records(record_id):
    file = Statement.query.get(record_id)
    file.status = StatementStatus.imported.value
    db.session.commit()

    importer = Factory.get(file.source)
    df = importer.read(f"{file_path}/{file.path}")
    records = importer.parse(df)
    importer.save(records)
