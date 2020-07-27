from flask_babel import _


def format_section(section_dict):
    """
    """
    section_formated = list()

    for id, name in set([(q['aspect_id'], q['name']) for q in section_dict]):
        aspect = {}
        aspect['id'] = id
        aspect['name'] = name

        questions = [q for q in section_dict if q['aspect_id'] == id]
        questions = list(sorted(questions, key=lambda item: item['order']))

        aspect['questions'] = questions

        section_formated.append(aspect)

    return list(sorted(section_formated, key=lambda item: item['id']))


def format_questions(questions):
    """
    """
    questions_formated = {}

    sections = ['start', 'validation', 'safety', 'monitoring']

    for section in sections:
        questions_formated[section] = [
            q for q in questions if q['section'] == section]
        questions_formated[section] = format_section(
            questions_formated[section])

    return questions_formated


def get_questions():
    """
    """
    questions = [
        {
            "aspect_id": 1,
            "order": "None",
            "section": "start",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Proof of framing",
            "question": "Have you kept a written record of the AI project, having as a minimum information who, what, why, how and when?",
            "example": "None",
            "suggestion": "Complete a document framing the subject as in the Proof of Framing tab."
        },
        {
            "aspect_id": 2,
            "order": "None",
            "section": "start",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Stakeholder participation",
            "question": "Were at least one sponsor, one developer and one end user involved in the framing and validation of the model?",
            "example": "None",
            "suggestion": "Include the different actors"
        },
        {
            "aspect_id": 3,
            "order": "None",
            "section": "start",
            "question_type": "boolean",
            "good_answer": "None",
            "name": "Social impact",
            "question": "Can the model have a social impact on a user?",
            "example": "Risk of job loss, refusal of a bank loan",
            "suggestion": "If you identify a social impact, please perform a bias analysis during validation."
        },
        {
            "aspect_id": 4,
            "order": 0,
            "section": "start",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Privacy and data protection",
            "question": "Have you considered ways to develop the AI system or train the model without (or with limited use of) potentially sensitive or personal data?",
            "example": "None",
            "suggestion": "If model training did not take place, compare the model performance with and sense sensitive data."
        },
        {
            "aspect_id": 4,
            "order": 1,
            "section": "start",
            "question_type": "boolean_plus_one",
            "good_answer": 1,
            "name": "Privacy and data protection",
            "question": "Where there is a data protection officer, have you engaged this person at an early stage in the process?",
            "example": "None",
            "suggestion": "Present the AI to the Data Protection Officer."
        },
        {
            "aspect_id": 5,
            "order": "None",
            "section": "start",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Justification",
            "question": "Has the justification for AI been validated by a third party actor with a data protection authority (DPO in the European Union)? If there is no equivalent, is AI beneficial to the end user?",
            "example": "None",
            "suggestion": "Present the AI and its justification to a third party actor."
        },
        {
            "aspect_id": 6,
            "order": 0,
            "section": "validation",
            "question_type": "numeric",
            "good_answer": "None",
            "name": "Sustainable, respect for the environment",
            "question": "How long (cumulated if several trainings) has the model been trained for?",
            "example": "None",
            "suggestion": "None"
        },
        {
            "aspect_id": 6,
            "order": 1,
            "section": "validation",
            "question_type": "list",
            "good_answer": "None",
            "name": "Sustainable, respect for the environment",
            "question": "In which country is the server used to train the model located?",
            "example": "None",
            "suggestion": "None"
        },
        {
            "aspect_id": 6,
            "order": 2,
            "section": "validation",
            "question_type": "numeric",
            "good_answer": "None",
            "name": "Sustainable, respect for the environment",
            "question": "Using the CO2 Evaluation module or the ML CO2 Impact site, can you indicate the amount of CO2 emitted?",
            "example": "None",
            "suggestion": "https://mlco2.github.io/impact/#act"
        },
        {
            "aspect_id": 7,
            "order": 0,
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Quality and integrity",
            "question": "Do you have processes in place to ensure the quality and integrity of your data within the project?",
            "example": "Data reliability indicators, a data validation phase with business experts.",
            "suggestion": "None"
        },
        {
            "aspect_id": 7,
            "order": 1,
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Quality and integrity",
            "question": "Have you carried out a data analysis phase?",
            "example": "None",
            "suggestion": "Use of the \"Dataset Analysis\" module to analyse the particularities of the data."
        },
        {
            "aspect_id": 8,
            "order": 0,
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Performance validation",
            "question": "Have the validation criteria been determined by the sponsors?",
            "example": "None",
            "suggestion": "None"
        },
        {
            "aspect_id": 8,
            "order": 1,
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Performance validation",
            "question": "Are the criteria met by the model?",
            "example": "None",
            "suggestion": "Use of the \"Performance\" module to analyze the performance of the model."
        },
        {
            "aspect_id": 9,
            "order": "None",
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Explanability",
            "question": "Are you aware of how the model works in general, which variables are most important?",
            "example": "None",
            "suggestion": "Use of the \"Explicability\" module to analyze model behavior."
        },
        {
            "aspect_id": 10,
            "order": "None",
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Interpretability",
            "question": "Have you tried to use the simplest and easiest interpretable model for the application in question? ",
            "example": "If you use a neural network for classification, have you tried a decision tree or a Random Forest before?",
            "suggestion": "During a next training session, try a simpler model to compare performances."
        },
        {
            "aspect_id": 11,
            "order": 0,
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Avoiding unfair bias",
            "question": "If a social impact is identified, have you defined on which attributes a person might be discriminated against?",
            "example": "Gender, age or marital status.",
            "suggestion": "None"
        },
        {
            "aspect_id": 11,
            "order": 1,
            "section": "validation",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Avoiding unfair bias",
            "question": "Have you analysed the potential biases on the attributes to be protected and validated that their incidence does not have a discriminatory impact?",
            "example": "None",
            "suggestion": "Use the \"Bias analysis\" module to analyze the biases of a model."
        },
        {
            "aspect_id": 12,
            "order": 0,
            "section": "safety",
            "question_type": "boolean",
            "good_answer": "None",
            "name": "Model Resilience",
            "question": "Have you identified potential forms of adverse attacks such as data pollution?",
            "example": "None",
            "suggestion": "https://github.com/IBM/adversarial-robustness-toolbox"
        },
        {
            "aspect_id": 12,
            "order": 1,
            "section": "safety",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Model Resilience",
            "question": "Have you tested extreme (rare) and common scenarios to see how the model behaves?",
            "example": "None",
            "suggestion": "Use of the \"Scenario testing\" module to test the model's behavior."
        },
        {
            "aspect_id": 13,
            "order": 0,
            "section": "safety",
            "question_type": "boolean_if_yes",
            "good_answer": 1,
            "name": "Emergency plan",
            "question": "In the event of a model malfunction, have you planned at least one procedure to ensure continuity of service for the AI? ",
            "example": "None",
            "suggestion": "Thinking about a backup procedure such as setting up a previous version of the model for example."
        },
        {
            "aspect_id": 13,
            "order": 1,
            "section": "safety",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Emergency plan",
            "question": "If so, have they been tested?",
            "example": "None",
            "suggestion": "Test the backup procedure(s)."
        },
        {
            "aspect_id": 14,
            "order": "None",
            "section": "safety",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "General Safety",
            "question": "Are you sure that the technologies used do not have any known security flaws? ",
            "example": "None",
            "suggestion": "Use the \"Python Security\" module if you use the Python language, to go further see the CVE Details site."
        },
        {
            "aspect_id": 15,
            "order": 0,
            "section": "monitoring",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Traceability",
            "question": "Is the technical pipeline documented?",
            "example": "None",
            "suggestion": "Documentation of the code and / or technical pipeline depending on the technologies used."
        },
        {
            "aspect_id": 15,
            "order": 1,
            "section": "monitoring",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Traceability",
            "question": "Do you have proof of validation of the AI prior to putting it into production?",
            "example": "None",
            "suggestion": "Create a document stipulating performance measures on the test set."
        },
        {
            "aspect_id": 16,
            "order": 0,
            "section": "monitoring",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Human Control",
            "question": "Has a recurring procedure for monitoring AI performance been put in place to ensure the viability of the model in the real world?",
            "example": "None",
            "suggestion": "Set up a recurring performance monitoring procedure."
        },
        {
            "aspect_id": 16,
            "order": 1,
            "section": "monitoring",
            "question_type": "boolean_plus_one",
            "good_answer": 1,
            "name": "Human Control",
            "question": "Is it possible for a user of the model to appeal on an AI prediction and for a human decision-maker to arbitrate on this appeal?",
            "example": "None",
            "suggestion": "Put at minimum, a contact so that the user can have a possibility to appeal if the prediction has a negative impact."
        },
        {
            "aspect_id": 17,
            "order": "None",
            "section": "monitoring",
            "question_type": "boolean",
            "good_answer": 1,
            "name": "Arbitration and recourse in case of negative impact",
            "question": "If a negative impact is identified, have you put in place an appropriate set of mechanisms to allow for recourse in the event of harm or adverse effects? ",
            "example": "None",
            "suggestion": "None"
        }
    ]

    return format_questions(questions)
