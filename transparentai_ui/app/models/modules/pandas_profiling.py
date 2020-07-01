from ... import db
import json

class ModulePandasProfiling(db.Model):
    """
    """
    __tablename__ = 'transparentai-module-pandas-profiling'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('transparentai-datasets.id'))
    dataset = db.relationship('Dataset', back_populates='module_pandas_profiling')

    status = db.Column(db.String, default='loading')
    path = db.Column(db.String)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModulePandasProfiling %s>' % (id)
