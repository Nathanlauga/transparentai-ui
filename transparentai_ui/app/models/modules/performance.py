from ... import db
from ...utils.models import dict_property, dict_property_setter
from ..base_model import BaseModel


class ModulePerformance(BaseModel):
    """
    """
    __tablename__ = 'transparentai-module-performance'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-datasets.id'))
    dataset = db.relationship('Dataset', back_populates='module_performance')

    status = db.Column(db.String, default='loading')
    _results = db.Column(db.String, default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    _default_fields = [
        "results",
        "status"
        "dataset_id"
    ]
    _hidden_fields = [
        "dataset"
    ]
    _readonly_fields = []

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModulePerformance %s>' % (id)

    @property
    def results(self):
        return dict_property(self._results)

    @results.setter
    def results(self, value):
        self._results = dict_property_setter(new_dict=value)
