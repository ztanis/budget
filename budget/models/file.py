import os.path as op
from flask_admin import form
from flask_admin.contrib import sqla

from budget.context import db

# Figure out base upload path
file_path = op.join(op.dirname(__file__), '../files')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))

    def __unicode__(self):
        return self.name
