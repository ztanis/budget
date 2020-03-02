from flask import flash
from flask_admin import BaseView, expose

from budget.classifiers.classifier import classify_unknown
from budget.models.category import Category
from sqlalchemy import func

from budget.models.record import Record


class GetStartedView(BaseView):
    @expose('/')
    def index(self):
        return self.render(
            'admin/get_started/index.html'
        )
