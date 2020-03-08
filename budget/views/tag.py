from  budget.context import db
from flask_admin.contrib import sqla


class TagAdmin(sqla.ModelView):
    column_list = ['name']
