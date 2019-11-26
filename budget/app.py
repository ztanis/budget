import flask_admin as admin

from budget.context import db, app
from budget.models.category import Category
from budget.models.file import File
from budget.models.record import Record
from budget.views.category import CategoryAdmin
from budget.views.file import FileView
from budget.views.record import RecordAdmin

# Create admin
admin = admin.Admin(app, name='Example: SQLAlchemy Association Proxy', template_mode='bootstrap3')
admin.add_view(FileView(File, db.session))
admin.add_view(RecordAdmin(Record, db.session))
admin.add_view(CategoryAdmin(Category, db.session))


if __name__ == '__main__':

    # Create DB
    # db.drop_all()
    db.create_all()

    # Start app
    app.run(debug=True)
