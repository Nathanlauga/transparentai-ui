from ... import db
from ...utils.models import dict_property, dict_property_setter
from ..base_model import BaseModel


class AIEvaluation(BaseModel):
    """
    """
    __tablename__ = 'transparentai-module-ai-evaluation'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey('transparentai-projects.id'))
    model = db.relationship('Model', back_populates='module_ai_evaluation')

    status = db.Column(db.String, default='init')

    _answers = db.Column(db.String, default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    _default_fields = [
        "answers",
        "status"
        "project_id"
    ]
    _hidden_fields = [
        "model"
    ]
    _readonly_fields = []

    def __repr__(self):
        id = 'None' if self.id is None else str(self.id)
        return '<ModuleAIEvaluation %s>' % (id)

    @property
    def answers(self):
        return dict_property(self._answers)

    @answers.setter
    def answers(self, value):
        self._answers = dict_property_setter(new_dict=value)
