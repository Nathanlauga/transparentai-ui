from ... import db
from ...utils.components import list_property, list_property_setter


class Model(db.Model):
    """
    """
    __tablename__ = 'transparentai-models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    path = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Model %r>' % self.name
