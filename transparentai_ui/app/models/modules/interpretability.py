from ... import db
from ...utils.models import dict_property


class ModuleInterpretability(db.Model):
    """
    """
    __tablename__ = 'transparentai-module-interpretability'

    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-models.id'))
    model = db.relationship('Model', back_populates='module_interpretability')

    status = db.Column(db.String, default='init')

    _variable_influence = db.Column(db.String, default='')
    explainer_path = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModuleInterpretability %s>' % (id)

    @property
    def variable_influence(self):
        return dict_property(self._variable_influence)

    @variable_influence.setter
    def variable_influence(self, value):
        self._variable_influence = str(value).replace("'", '"')