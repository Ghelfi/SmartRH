from numpy.lib.index_tricks import index_exp
from sqlalchemy.sql.elements import and_
from .tables import Role, Status, Field, ExtractionAlgorithm, Candidate, CV, Event, User, get_candidate, get_extraction_algorithm, get_field, get_role
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
        candidates.append(candidate)
        app.add_to_db(candidate)


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
        users.append(user)

    # Insert CVs
    number_of_cvs = 10
    status = [e for e in app.query(Status)]
    cvs = []
    import datetime as dt
    for ind_cv in range(number_of_cvs):
        cv = CV(
            filename = f"dummy_cv_{ind_cv}",
            date_submission = int(dt.datetime.now().strftime('%s')),
            register = users[ind_cv%len(users)],
            status = status[ind_cv%len(status)],
            candidate= candidates[ind_cv%len(candidates)]
        )
        app.add_to_db(cv)
        cvs.append(cv)



    # Insert Events and Links
    import numpy as np
    skill_list = ['tf', 'tensorflow', 'Tensorflow', 'TF', 'PyTorch', 'CUDA', 'GPU', 'C++', 'Python', 'TF2.X', 'Gestion de Projet', 'Management', 'French', 'English']
    company_list = ['World Corp', 'Local Corp', 'LC', 'ZonZon', 'Oogle', 'Tech University', 'MidTech University']
    position_list = ['Data Scientist', 'data Engineer', 'Dev', 'Manager', 'Data God', 'Intern']
    
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
            company = np.random.choice(company_list)
            position_event = Event(cv=cv, algo=extractor, field=get_field(app, 'position'), value = position)
            company_event = Event(cv=cv, algo=extractor, field=get_field(app, 'company'), value = company)
            app.add_to_db(position_event)
            app.add_to_db(company_event)
            pass

