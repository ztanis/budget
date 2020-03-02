from flask import flash
from flask_admin import BaseView, expose

from budget.classifiers.classifier import classify_unknown
from budget.models.category import Category
from sqlalchemy import func

from budget.models.record import Record


class CategorizationView(BaseView):
    @expose('/')
    def index(self):
        return self.render(
            'admin/categorization/index.html', **self._stats()
        )

    @expose('/classify')
    def action_categorize(self):
        # TODO add statistics for categorization
        classify_unknown()
        flash("Categorization was finished successfully")
        return self.render(
            'admin/categorization/index.html', **self._stats()
        )

    def _stats(self):
        return dict(
            categories_num=Category.query.count(),
            categorized_confirmed_records=Record.query.filter(Record.category_id != None).filter(Record.is_confirmed == True).count(),
            categorized_not_confirmed_records=Record.query.filter(Record.category_id != None).filter(Record.is_confirmed == False).count(),
            uncategorized_records=Record.query.filter(Record.category_id == None).count()
        )
