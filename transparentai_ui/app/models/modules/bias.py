from ... import db
from ...utils.models import dict_property


class ModuleBias(db.Model):
    """
    """
    __tablename__ = 'transparentai-module-bias'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-datasets.id'))
    dataset = db.relationship('Dataset', back_populates='module_bias')

    status = db.Column(db.String, default='loading')
    _results = db.Column(db.String, default='')
    _privileged_group = db.Column(db.String, default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModuleBias %s>' % (id)

    @property
    def results(self):
        return dict_property(self._results)

    @results.setter
    def results(self, value):
        self._results = str(value).replace("'", '"')

    @property
    def privileged_group(self):
        return dict_property(self._privileged_group)

    @privileged_group.setter
    def privileged_group(self, value):
        self._privileged_group = str(value).replace("'", '"')