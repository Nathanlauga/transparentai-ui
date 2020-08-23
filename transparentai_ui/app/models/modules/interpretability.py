from ... import db
from ...utils.models import dict_property
from ..base_model import BaseModel


class ModuleInterpretability(BaseModel):
    """
    """
    __tablename__ = 'transparentai-module-interpretability'

    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-models.id'))
    model = db.relationship('Model', back_populates='module_interpretability')

    # Todo : custom nrows global influence
    # nrows = db.Column(db.Integer, default=1000)

    status = db.Column(db.String, default='init')

    _variable_influence = db.Column(db.String, default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    _default_fields = [
        "variable_influence",
        "status",
        "model_id",
        # "nrows"
    ]
    _hidden_fields = [
        "model"
    ]
    _readonly_fields = []

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModuleInterpretability %s>' % (id)

    @property
    def variable_influence(self):
        return dict_property(self._variable_influence)

    @variable_influence.setter
    def variable_influence(self, value):
        self._variable_influence = str(value).replace("'", '"')
