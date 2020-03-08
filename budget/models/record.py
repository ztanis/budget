from sqlalchemy import UniqueConstraint

from  budget.context import db
from budget.models.tag import Tag


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=True)
    category = db.relationship("Category")
    account = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=False)
    comment = db.Column(db.Text(), nullable = False)
    recorded_at = db.Column(db.DateTime(), nullable = False)
    created_at = db.Column(db.DateTime(), nullable = False)
    updated_at = db.Column(db.DateTime(), nullable = False)
    is_confirmed = db.Column(db.Boolean, default=False)
    tags = db.relationship(Tag, secondary='record_tag')
    __table_args__ = (
        UniqueConstraint('name', 'account', 'recorded_at', 'amount', name='uix_1'),
    )


