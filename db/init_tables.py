from .tables import Role, Status, Field, ExtractionAlgorithm, Candidat, CV, Event, User
from flask_sqlalchemy import SQLAlchemy, SessionBase, sqlalchemy
from app import App


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

    for extraction_algorithm_dict in conf['ExtractionAlgorithms']:
        algo = ExtractionAlgorithm(name=extraction_algorithm_dict['name'], version=extraction_algorithm_dict['version'])
        app.add_to_db(algo)
    
def fill_tables_with_dummy_examples(app: App):

    # Insert Candidates
    candidate_names = [
        ('Antoine', 'Dupont'),
        ('Julien', 'Marchand'),
        ('Romain', "N'Tamack")
    ]

    for candidate_name in candidate_names:
        candidat = Candidat(name=candidate_name[1], 
            firstname=candidate_name[0],
            phone_number="0699999999", 
            email="{}.{}@mail.com".format(candidate_name[0], candidate_name[1])
            )
        app.add_to_db(candidat)


    # Insert Users
    user_names = [
        'Martin Durand',
        'Geraldine Gérard',
        'Thibault User',
        'Martine Martin',
        'Gérard Dupont',
    ]
    roles = [e for e in app.query(Role)]
    for ind, user_name in enumerate(user_names):
        user = User(name=user_name, role=roles[ind%len(roles)])
        app.add_to_db(user)

