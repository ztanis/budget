from flask import flash
from flask_admin.actions import action
from flask_admin.contrib import sqla

from budget.models.record import Record
from budget.context import db


class RecordAdmin(sqla.ModelView):
    """ Flask-admin can not automatically find a association_proxy yet. You will
        need to manually define the column in list_view/filters/sorting/etc.
        Moreover, support for association proxies to association proxies
        (e.g.: keywords_values) is currently limited to column_list only."""

    column_list = ["recorded_at", 'name', 'amount', 'category', 'is_confirmed']
    column_sortable_list = ['recorded_at', 'name', 'amount', 'category', 'is_confirmed']
    column_filters = ('recorded_at', 'name', 'account', 'category', 'is_confirmed')

    form_columns = ('name', 'account', 'amount', 'comment', 'category', 'created_at', 'updated_at', 'recorded_at')
    column_editable_list = ['category', 'is_confirmed']

    @action('confirm', 'Confirm Category', 'Are you sure you want to confirm records?')
    def action_confirm(self, ids):
        for record_id in ids:
            Record.query.filter_by(id=record_id).update({
                'is_confirmed': True
            })
        db.session.commit()
        flash(f"{len(ids)} records were confirmed")
