from ... import db
from ..base_model import BaseModel


class ModuleSustainable(BaseModel):
    """
    """
    __tablename__ = 'transparentai-module-sustainable'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-projects.id'))
    project = db.relationship('Project', back_populates='module_sustainable')

    status = db.Column(db.String, default='init')
    time = db.Column(db.Float)
    location = db.Column(db.String)
    watts = db.Column(db.Integer, default=250)
    result = db.Column(db.Float)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    _default_fields = [
        "result",
        "time",
        "location",
        "watts",
        "status"
        "project_id"
    ]
    _hidden_fields = [
        "project"
    ]
    _readonly_fields = []

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModuleSustainable %s>' % (id)