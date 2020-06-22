from ... import db


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

    def __repr__(self):
        return '<Dataset %r>' % self.name

    @property
    def protected_attr(self):
        return [str(x) for x in self._protected_attr.split(';')][1:]

    @protected_attr.setter
    def protected_attr(self, value):
        if self._protected_attr is None:
            self._protected_attr = ''
            
        if type(value) == list:
            for v in value:
                self._protected_attr += ';%s' % str(v)
        else:
            self._protected_attr += ';%s' % str(value)

    @property
    def model_columns(self):
        return [str(x) for x in self._model_columns.split(';')]

    @protected_attr.setter
    def model_columns(self, value):
        if self._model_columns is None:
            self._model_columns = ''

        if type(value) == list:
            for v in value:
                self._model_columns += ';%s' % v
        else:
            self._model_columns += ';%s' % value
