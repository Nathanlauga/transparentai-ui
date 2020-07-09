from .. import db
from ..utils.models import list_property, list_property_setter
from .base_model import BaseModel

from ..models.modules import ModuleInterpretability

class Model(BaseModel):
    """
    """
    __tablename__ = 'transparentai-models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    path = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String)

    dataset_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-datasets.id'))
    dataset = db.relationship('Dataset')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # Modules
    module_interpretability = db.relationship(
        'ModuleInterpretability', uselist=False, back_populates='model', cascade='save-update, merge, delete')

    
    _default_fields = [
        "name",
        "path",
        "file_type",
        "dataset_id"
    ]
    _hidden_fields = [
        "module_interpretability"
    ]
    _readonly_fields = []


    def __repr__(self):
        return '<Model %r>' % self.name
