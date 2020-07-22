from ... import db
import json
from ..base_model import BaseModel

class ModulePandasProfiling(BaseModel):
    """
    """
    __tablename__ = 'transparentai-module-pandas-profiling'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('transparentai-datasets.id'))
    dataset = db.relationship('Dataset', back_populates='module_pandas_profiling')

    minimal = db.Column(db.Boolean, default=True)
    explorative = db.Column(db.Boolean, default=True)
    nrows = db.Column(db.Integer)

    status = db.Column(db.String, default='loading')
    path = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    _default_fields = [
        "path",
        "minimal",
        "explorative",
        "nrows",
        "status"
        "dataset_id"
    ]
    _hidden_fields = [
        "dataset"
    ]
    _readonly_fields = []


    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModulePandasProfiling %s>' % (id)
