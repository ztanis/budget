from  budget.context import db
from flask_admin.contrib import sqla

class CategoryAdmin(sqla.ModelView):
    column_list = ['id', 'name']
