from .. import db
from ..utils.models import list_property, list_property_setter
from .base_model import BaseModel


class Dataset(BaseModel):
    """
    """
    __tablename__ = 'transparentai-datasets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    path = db.Column(db.String, nullable=False)
    _columns = db.Column(db.String, default='')
    target = db.Column(db.String)
    score = db.Column(db.String)
    model_type = db.Column(db.String)
    _protected_attr = db.Column(db.String, default='')
    _model_columns = db.Column(db.String, default='')
    length = db.Column(db.Integer)
    sep = db.Column(db.String, default=',')
    encoding = db.Column(db.String, default='utf_8')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    project_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-projects.id'))
    project = db.relationship('Project')

    # Modules
    model = db.relationship(
        'Model', uselist=False, back_populates='dataset', cascade='save-update, merge, delete')

    # Modules
    module_pandas_profiling = db.relationship(
        'ModulePandasProfiling', uselist=False, back_populates='dataset', cascade='save-update, merge, delete')
    module_performance = db.relationship(
        'ModulePerformance', uselist=False, back_populates='dataset', cascade='save-update, merge, delete')
    module_bias = db.relationship(
        'ModuleBias', uselist=False, back_populates='dataset', cascade='save-update, merge, delete')

    _default_fields = [
        "name",
        "path",
        "columns",
        "target",
        "score",
        "model_type",
        "protected_attr",
        "model_columns",
        "length",
        "project_id",
        "sep",
        "encoding"
    ]
    _hidden_fields = [
        "model",
        "project",
        "module_pandas_profiling",
        "module_performance",
        "module_bias",
    ]
    _readonly_fields = []

    def __repr__(self):
        return '<Dataset %r>' % self.name

    @property
    def columns(self):
        return list_property(self._columns, unique=True)

    @columns.setter
    def columns(self, value):
        self._columns = list_property_setter(
            self._columns, value)

    @property
    def protected_attr(self):
        return list_property(self._protected_attr, unique=True)

    @protected_attr.setter
    def protected_attr(self, value):
        self._protected_attr = list_property_setter(
            self._protected_attr, value)

    @property
    def model_columns(self):
        return list_property(self._model_columns, unique=True)

    @model_columns.setter
    def model_columns(self, value):
        self._model_columns = list_property_setter(
            self._model_columns, value)
