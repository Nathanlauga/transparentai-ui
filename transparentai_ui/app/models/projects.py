from .. import db
from ..utils.models import list_property, list_property_setter
from .base_model import BaseModel


class Project(BaseModel):
    """
    """
    __tablename__ = 'transparentai-projects'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String)
    name = db.Column(db.String, unique=True, nullable=False)
    _members = db.Column(db.String, default='')
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # Modules
    dataset = db.relationship(
        'Dataset', uselist=False, back_populates='project')

    
    _default_fields = [
        "name",
        "desc",
        "members",
    ]
    _hidden_fields = [
        "dataset"
    ]
    _readonly_fields = []


    def __repr__(self):
        return '<Project %r>' % self.name

    @property
    def members(self):
        return list_property(self._members, unique=True)

    @members.setter
    def members(self, value):
        self._members = list_property_setter(
            self._members, value)
