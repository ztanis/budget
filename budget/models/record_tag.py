from sqlalchemy import UniqueConstraint

from  budget.context import db


class RecordTag(db.Model):
    record_id = db.Column(
        db.Integer,
        db.ForeignKey('record.id'),
        primary_key=True)

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tag.id'),
        primary_key=True)
