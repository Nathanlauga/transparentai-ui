from ... import db
import json

from ...models.components import Model, Dataset 


class Module(db.Model):
    """
    """
    __tablename__ = 'transparentai-models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ref_id = db.Column(db.Integer)
    json = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Module %r %i>' % (self.name, self.id)

    @property
    def ref_obj(self):
        # ['evaluation-form', 'ml-canvas', 'bias-report', 'performance-report',
        #     'pandas-profiling', 'scenario', 'interpretability', 'safety', 'sustainable']

        if self.name in ['evaluation-form', 'ml-canvas', 'sustainable','safety']:
            obj = None
            
        elif self.name in ['bias-report', 'performance-report','pandas-profiling']:
            obj = Dataset.query.filter_by(id=self.ref_id).first()

        elif self.name in ['scenario', 'interpretability']:
            obj = Model.query.filter_by(id=self.ref_id).first()

        return obj
