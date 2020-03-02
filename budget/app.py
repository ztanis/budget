import flask_admin as admin

from budget.context import db, app
from budget.models.category import Category
from budget.models.statement import Statement
from budget.models.record import Record
from budget.views.categorization import CategorizationView
from budget.views.category import CategoryAdmin
from budget.views.get_started import GetStartedView
from budget.views.statement import StatementView
from budget.views.record import RecordAdmin

# Create admin
admin = admin.Admin(app, name='Budget', template_mode='bootstrap3')
admin.add_view(GetStartedView(name='Get Started', endpoint='get_started'))
admin.add_view(StatementView(Statement, db.session))
admin.add_view(RecordAdmin(Record, db.session))
admin.add_view(CategoryAdmin(Category, db.session))
admin.add_view(CategorizationView(name='Categorization', endpoint='categorization'))


if __name__ == '__main__':

    # Create DB
    #db.drop_all()
    db.create_all()

    # Start app
    app.run(debug=True)
