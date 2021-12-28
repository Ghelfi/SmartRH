import pdb
from numpy.lib.index_tricks import index_exp
from sqlalchemy.sql.elements import and_
from .tables import Link, Role, Status, Field, ExtractionAlgorithm, \
        Candidate, CV, Event, User, get_candidate, get_extraction_algorithm, \
        get_field, get_role, get_cv, get_cv_from_cvobject, get_candidate_from_candidateobject, \
        get_user_from_userobject
from flask_sqlalchemy import SQLAlchemy, SessionBase, sqlalchemy
from app import App
from extraction import normalize_skill_list


def initialize_tables(app: App, conf: dict):
    for role_dict in conf['Roles']:
        role = Role(name=role_dict['name'], value=role_dict['value'])
        app.add_to_db(role)

    for status_dict in conf['Status']:
        status = Status(name=status_dict['name'])
        app.add_to_db(status)

    for field_dict in conf['Fields']:
        field = Field(name=field_dict['name'])
        app.add_to_db(field)

    
    extractor_in_db = app.query(ExtractionAlgorithm).filter(and_(ExtractionAlgorithm.name == app.extractor.name, ExtractionAlgorithm.version == app.extractor.version)).all()
    if len(extractor_in_db) == 0:
        extractor_model = ExtractionAlgorithm(
            name = app.extractor.name,
            version = app.extractor.version,
        )
        app.add_to_db(extractor_model)
    
def generate_mock_data(app: App):

    # Insert Candidates
    candidate_names = [
        ('Antoine', 'Dupont'),
        ('Julien', 'Marchand'),
        ('Romain', "N'Tamack")
    ]
    candidates = []
    for candidate_name in candidate_names:
        candidate = Candidate(name=candidate_name[1], 
            firstname=candidate_name[0],
            phone_number="0699999999", 
            email="{}.{}@mail.com".format(candidate_name[0], candidate_name[1])
            )
        app.add_to_db(candidate)
        candidates.append(get_candidate_from_candidateobject(app, candidate))



    # Insert Users
    user_names = [
        'Martin Durand',
        'Geraldine Gérard',
        'Thibault User',
        'Martine Martin',
        'Gérard Dupont',
    ]
    roles = [e for e in app.query(Role)]
    users = []
    for ind, user_name in enumerate(user_names):
        user = User(name=user_name, role=roles[ind%len(roles)])
        app.add_to_db(user)
        users.append(get_user_from_userobject(app, user))

    # Insert CVs
    number_of_cvs = 10
    status = [e for e in app.query(Status)]
    cvs = []
    import datetime as dt
    for ind_cv in range(number_of_cvs):
        cv = CV(
            filename = f"dummy_cv_{ind_cv}",
            date_submission = int(dt.datetime.now().strftime('%s')),
            dropper_id = users[ind_cv%len(users)].id,
            status_id = status[ind_cv%len(status)].id,
            candidate_id= candidates[ind_cv%len(candidates)].id
        )
        app.add_to_db(cv)
        cvs.append(get_cv_from_cvobject(app, cv))



    # Insert Events and Links
    import numpy as np
    skill_list = ['tf', 'tensorflow', 'Tensorflow', 'TF', 'PyTorch', 'CUDA', 'GPU', 'C++', 'Python', 'TF2.X', 'Gestion de Projet', 'Management', 'French', 'English']
    company_list = ['World Corp', 'Local Corp', 'LC', 'ZonZon', 'Oogle', 'Tech University', 'MidTech University']
    position_list = ['Data Scientist', 'data Engineer', 'Dev', 'Manager', 'Data God', 'Intern']
    other_list = ["Hiking", "Reading", "Football", "Travel", "Informatics"]

    extractor = get_extraction_algorithm(app, name=app.extractor.name, version=app.extractor.version)
    
    for cv in cvs:
        number_of_exp: int = np.random.randint(1,5)
        start_date = dt.datetime.now() - dt.timedelta(days=int(365.25*max(1,number_of_exp+np.random.randint(2))))
        stop_date = None
        if number_of_exp > 1:
            time_between_actual_date_and_midsection = int(0.5*(dt.datetime.now() - start_date).days)
            stop_date = start_date + dt.timedelta(days=np.random.randint(int(0.25*time_between_actual_date_and_midsection), time_between_actual_date_and_midsection))
        for ind_exp, exp in enumerate(range(number_of_exp)):
            if ind_exp > 0:
                start_date = stop_date
                time_between_actual_date_and_midsection = int(0.5*(dt.datetime.now() - start_date).days)
                stop_date = start_date + dt.timedelta(days=np.random.randint(int(0.25*time_between_actual_date_and_midsection), time_between_actual_date_and_midsection))
            if ind_exp == number_of_exp - 1:
                stop_date = None
            
            position = np.random.choice(position_list)
            skills = normalize_skill_list(np.random.choice(skill_list, size=np.random.randint(1, 5)).tolist())
            others = normalize_skill_list(np.random.choice(other_list, size=np.random.randint(1, 3)).tolist())
            company = np.random.choice(company_list)
            position_event = Event(cv=cv, algo=extractor, field=get_field(app, 'position'), value = position)
            company_event = Event(cv=cv, algo=extractor, field=get_field(app, 'company'), value = company)
            skill_events = [Event(cv=cv, algo=extractor, field=get_field(app, 'skill'), value = e) for e in skills]
            other_events = [Event(cv=cv, algo=extractor, field=get_field(app, 'other'), value = e) for e in others]

            event_list = [company_event, position_event]
            event_list.extend(skill_events)
            event_list.extend(other_events)
            [app.add_to_db(e) for e in event_list]
            for ind_event_1, event_1 in enumerate(event_list):
                for ind_event_2 in range(ind_event_1+1, len(event_list)):
                    link = Link(event_id_one=event_list[ind_event_1].id, event_id_two=event_list[ind_event_2].id)
                    app.add_to_db(link)

