import os.path as op
from enum import Enum

from budget.context import db

# Figure out base upload path
file_path = op.join(op.dirname(__file__), '../files')


class StatementStatus(Enum):
    uploaded = 'uploaded'
    imported = 'imported'


class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))
    status = db.Column(db.Unicode(16), default=StatementStatus.uploaded.value)

    def __unicode__(self):
        return self.name
