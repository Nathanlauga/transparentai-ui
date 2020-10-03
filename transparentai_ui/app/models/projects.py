from .. import db
from ..utils.models import list_property, list_property_setter, dict_property, dict_property_setter
from .base_model import BaseModel

from ..src import get_questions


class Project(BaseModel):
    """
    """
    __tablename__ = 'transparentai-projects'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String)
    name = db.Column(db.String, unique=True, nullable=False)
    _members = db.Column(db.String, default='')
    _answers = db.Column(db.String, default='')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime,
                           server_default=db.func.now(),
                           server_onupdate=db.func.now())

    # Modules
    dataset = db.relationship('Dataset',
                              uselist=False,
                              back_populates='project',
                              cascade='save-update, merge, delete')
    module_sustainable = db.relationship('ModuleSustainable',
                                         uselist=False,
                                         back_populates='project',
                                         cascade='save-update, merge, delete')

    _default_fields = ["name", "desc", "members", "answers", "n_answered"]
    _hidden_fields = ["dataset"]
    _readonly_fields = []

    def __repr__(self):
        return '<Project %r>' % self.name

    @property
    def members(self):
        return list_property(self._members, unique=True)

    @members.setter
    def members(self, value):
        self._members = list_property_setter(self._members, value)

    @property
    def answers(self):
        return dict_property(self._answers)

    @answers.setter
    def answers(self, value):
        self._answers = dict_property_setter(new_dict=value)

    @property
    def n_answered(self):
        if self.answers is None:
            return {'total': 0}
        elif len(self.answers) == 0:
            return {'total': 0}

        questions = get_questions()
        questions_by_section = [(k, elem) for k, section in questions.items()
                                for elem in section]
        sections = list(questions.keys())

        n_answered = {}
        total = 0
        to_improve = 0
        good_answers = 0

        for section in sections:
            n_answered[section] = 0

        for section, question in questions_by_section:
            answer = self.answers[str(question['id'])]

            is_answered = sum([e == 'None' for e in answer]) == 0
            if is_answered:
                n_answered[section] = n_answered[section] + 1
                total += 1

            is_to_improve = sum(
                [(e == 'no') & (q['good_answer'] == 1)
                 for (e, q) in zip(answer, question['questions'])]) > 0
            if is_to_improve:
                to_improve += 1

            is_good = sum([(e == 'yes') & (q['good_answer'] == 1)
                           for (e, q) in zip(answer, question['questions'])
                           ]) > 0
            if is_good:
                good_answers += 1

        n_answered['total'] = total
        n_answered['to_improve'] = to_improve
        n_answered['good_answers'] = good_answers

        # It corresponds to the number of answer for question that do not
        # requires a good answer or an answer to improve.
        n_answered['ignored'] = total - to_improve - good_answers

        return n_answered

    @property
    def n_questions(self):
        n_questions = {}
        questions = get_questions()

        for section, q_list in questions.items():
            n_questions[section] = len(q_list)

        n_questions['total'] = sum([n for n in n_questions.values()])

        return n_questions

    @property
    def prct_answered(self):
        if self.answers is None:
            return {'total': 0}
        elif len(self.answers) == 0:
            return {'total': 0}

        prct_answered = {}

        for section in self.n_questions.keys():
            prct_answered[section] = 100 * self.n_answered[
                section] / self.n_questions[section]

        return prct_answered

    @property
    def answers_eu_requirement(self):
        answers_eu_requirement = {}

        questions = get_questions()
        questions = [(elem['eu_requirement'], elem)
                     for k, section in questions.items() for elem in section]

        for req in set([e for (e, _) in questions]):
            answers_eu_requirement[req] = {
                'n_questions': 0,
                'n_answered': 0,
                'n_good': 0,
                'n_to_improve': 0,
                'prct_answered': 0,
                'prct_good': 0,
                'prct_to_improve': 0,
            }

        for req, question in questions:
            answer = self.answers[str(question['id'])]

            answers_eu_requirement[req]['n_questions'] += 1

            is_answered = sum([e == 'None' for e in answer]) == 0

            if is_answered:
                answers_eu_requirement[req]['n_answered'] += 1

            is_to_improve = sum(
                [(e == 'no') & (q['good_answer'] == 1)
                 for (e, q) in zip(answer, question['questions'])]) > 0

            if is_to_improve:
                answers_eu_requirement[req]['n_to_improve'] += 1

            is_good = sum([(e == 'yes') & (q['good_answer'] == 1)
                           for (e, q) in zip(answer, question['questions'])
                           ]) > 0
            if is_good:
                answers_eu_requirement[req]['n_good'] += 1

        for req in answers_eu_requirement.keys():
            answers_eu_requirement[req][
                'prct_answered'] = answers_eu_requirement[req][
                    'n_answered'] / answers_eu_requirement[req]['n_questions']
            answers_eu_requirement[req]['prct_good'] = answers_eu_requirement[
                req]['n_good'] / answers_eu_requirement[req]['n_questions']
            answers_eu_requirement[req][
                'prct_to_improve'] = answers_eu_requirement[req][
                    'n_to_improve'] / answers_eu_requirement[req]['n_questions']

        return answers_eu_requirement
