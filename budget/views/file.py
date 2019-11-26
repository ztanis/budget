import os.path as op
from flask_admin import form
from flask_admin.contrib import sqla

from budget.context import db

# Figure out base upload path
file_path = op.join(op.dirname(__file__), '../files')

class FileView(sqla.ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'path': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'path': {
            'label': 'File',
            'base_path': file_path,
            'allow_overwrite': False
        }
    }
