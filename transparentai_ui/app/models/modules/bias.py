from ... import db
import json

class ModuleBias(db.Model):
    """
    """
    __tablename__ = 'transparentai-module-bias'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('transparentai-datasets.id'))
    dataset = db.relationship('Dataset', back_populates='module_bias')

    status = db.Column(db.String, default='loading')
    _results = db.Column(db.String, default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<ModuleBias %i>' % (self.id)

    @property
    def results(self):
        if (str(self._results) == ''):
            return {}
        return json.loads(str(self._results))

    @results.setter
    def results(self, value):
        self._results = str(value)

