from ... import db
from ...utils.components import list_property, list_property_setter

from ...models.modules import ModulePandasProfiling

class Dataset(db.Model):
    """
    """
    __tablename__ = 'transparentai-datasets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    path = db.Column(db.String, nullable=False)
    target = db.Column(db.String)
    score = db.Column(db.String)
    _protected_attr = db.Column(db.String, default='')
    _model_columns = db.Column(db.String, default='')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # Modules
    module_pandas_profiling = db.relationship(
        'ModulePandasProfiling', uselist=False, back_populates='dataset')

    def __repr__(self):
        return '<Dataset %r>' % self.name

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
