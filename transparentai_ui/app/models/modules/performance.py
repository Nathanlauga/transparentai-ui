from ... import db
from ...utils.models import dict_property


class ModulePerformance(db.Model):
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

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModulePerformance %s>' % (id)

    @property
    def results(self):
        return dict_property(self._results)

    @results.setter
    def results(self, value):
        self._results = str(value).replace("'", '"')
