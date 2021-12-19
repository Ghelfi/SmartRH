from .tables import Role, Status, Field, ExtractionAlgorithm
from flask_sqlalchemy import SQLAlchemy, SessionBase, sqlalchemy


def initialize_tables(session: SessionBase, conf: dict):
    try:
        for role_dict in conf['Roles']:
            role = Role(name=role_dict['name'], value=role_dict['value'])
            session.add(role)

        for status_dict in conf['Status']:
            status = Status(name=status_dict['name'])
            session.add(status)

        for field_dict in conf['Fields']:
            field = Field(name=field_dict['name'])
            session.add(field)

        for extraction_algorithm_dict in conf['ExtractionAlgorithms']:
            algo = ExtractionAlgorithm(name=extraction_algorithm_dict['name'], version=extraction_algorithm_dict['version'])
            session.add(algo)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        pass