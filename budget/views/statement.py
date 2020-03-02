import os.path as op

from flask import flash
from flask_admin import form
from flask_admin.actions import action
from flask_admin.contrib import sqla

# Figure out base upload path
from budget import sources

file_path = op.join(op.dirname(__file__), '../files')


class StatementView(sqla.ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'path': form.FileUploadField
    }

    form_create_rules = ('source', 'path')
    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'path': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': False
        }
    }

    form_choices = {
        'source': [('cb', 'Commerzbank')]
    }

    @action('import', 'Import')
    def action_import(self, ids):
        for record_id in ids:
            sources.import_records(record_id)
        flash(f"{len(ids)} file(s) were imported")


