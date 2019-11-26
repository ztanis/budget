from budget.importers.cb import CBImporter
from budget.models.file import File
from budget.models.file import file_path

def import_records():
    files = File.query.all()
    importers = {
        'cb': CBImporter()
    }
    for file in files:
        importers['cb'].parse(f"{file_path}/{file.path}")
