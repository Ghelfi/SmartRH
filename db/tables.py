from app import my_app
from flask_sqlalchemy import SQLAlchemy
from app import App
from sqlalchemy.sql.elements import and_


db: SQLAlchemy = my_app.db

class Candidate(db.Model):
    __tablename__ = "candidates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=True, index=True)
    firstname = db.Column(db.String(40), unique=False, nullable=True)
    phone_number = db.Column(db.String(15), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return (
            f"<Candidate(id={self.id}, "
            f"user_name={self.name}, "
            f"user_firstname={self.firstname}, "
            f"phone_number={self.phone_number}, "
            f"email={self.email}, "
            f")>"
        )

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return (
            f"<Role(id={self.id}, "
            f"name={self.name}, "
            f"value={self.value}, "
            f")>"
        )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role')

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name={self.name}, "
            f"role={self.role.name}, "
            f")>"
        )

class Status(db.Model):
    __tablename__ = "status"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return (
            f"<Status(id={self.id}, "
            f"name={self.name}, "
            f")>"
        )

class CV(db.Model):
    __tablename__ = "cvs"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    date_submission = db.Column(db.Integer, unique=False, nullable=False, index=True)
    dropper_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)   

    register = db.relationship('User')
    status = db.relationship('Status')
    candidate = db.relationship('Candidate')

    def __repr__(self):
        return (
            f"<CV(id={self.id}, "
            f"filename={self.filename}, "
            f"date_submission={self.date_submission}, "
            f"register_by={self.register.name}, "
            f"status={self.status.name}, "
            f")>"
        )

class ExtractionAlgorithm(db.Model):
    __tablename__ = 'algorithms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    version = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return (
            f"<ExtractionAlgorithm(id={self.id}, "
            f"name={self.name}, "
            f"version={self.version}, "
            f")>"
        )

class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    def __repr__(self):
        return (
            f"<Field(id={self.id}, "
            f"name={self.name}, "
            f")>"
        )

class ExperienceType(db.Model):
    __tablename__ ="experience_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    def __repr__(self):
        return (
            f"<ExperienceType(id={self.id}, "
            f"name={self.name}, "
            f")>"
        )

class Experience(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False)
    algo_id = db.Column(db.Integer, db.ForeignKey('algorithms.id'), nullable=False)
    experience_type_id = db.Column(db.Integer, db.ForeignKey('experience_types.id'), nullable=False)
    start_date =  db.Column(db.Integer, unique=False, nullable=True, index=True)
    stop_date =  db.Column(db.Integer, unique=False, nullable=True, index=True)

    cv = db.relationship('CV')
    algo = db.relationship('ExtractionAlgorithm')
    experience_type = db.relationship('ExperienceType')

    def __repr__(self):
        return (
            f"<Experience(id={self.id}, "
            f"cv_filename={self.cv.filename}, "
            f"type={self.experience_type.name}, "
            f"extraction_algorithm={self.algo.name} v{self.algo.version}, "
            f"start_date={self.start_date}, "
            f"stop_date={self.stop_date}, "
            f")>"
        )

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer, db.ForeignKey('experiences.id'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)
    value = db.Column(db.String(50), unique=False, nullable=False, index=True)
   
    experience = db.relationship('Experience')
    field = db.relationship('Field')

    def __repr__(self):
        return (
            f"<Event(id={self.id}, "
            f"type={self.field.name}, "
            f"value={self.value}, "
            f")>"
        )

# class Link(db.Model):
#     __tablename__ = "links"
#     id = db.Column(db.Integer, primary_key=True)
#     event_id_one = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
#     event_id_two = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

#     event_one = db.relationship("Event", foreign_keys=[event_id_one])
#     event_two = db.relationship("Event", foreign_keys=[event_id_two])


def get_field(app: App, name: str)-> Field:
    return app.query(Field).filter(Field.name == name.lower()).first()

def get_role(app: App, name: str)-> Role:
    return app.query(Role).filter(Role.name == name.lower()).first()

def get_extraction_algorithm(app: App, name: str, version: str)-> ExtractionAlgorithm:
    return app.query(ExtractionAlgorithm).filter(and_(ExtractionAlgorithm.name == name, ExtractionAlgorithm.version == version)).first()

def get_candidate(app: App, name: str, firstname: str, phone_number:str, email: str)-> Candidate:
    return app.query(Candidate).filter(
        and_(
            Candidate.name == name, 
            Candidate.firstname == firstname,
            Candidate.phone_number == phone_number,
            Candidate.email == email,
            )
        ).first()

def get_cv(app: App, filename:str, date_submission:int, dropper_id:int, candidate_id:int, status_id:int)-> CV:
    return app.query(CV).filter(
        and_(
            CV.filename == filename,
            CV.date_submission == date_submission,
            CV.dropper_id == dropper_id,
            CV.candidate_id == candidate_id,
            CV.status_id == status_id
        )
    ).first()

def get_cv_from_cvobject(app:App, cv:CV)-> CV:
    return app.query(CV).filter(
        and_(
            CV.filename == cv.filename,
            CV.dropper_id == cv.dropper_id,
            CV.candidate_id == cv.candidate_id,
            CV.status_id == cv.status_id
        )
    ).first()

def get_candidate_from_candidateobject(app: App, candidate: Candidate)-> Candidate:
    return app.query(Candidate).filter(
        and_(
            Candidate.name == candidate.name, 
            Candidate.firstname == candidate.firstname,
            Candidate.phone_number == candidate.phone_number,
            Candidate.email == candidate.email,
            )
        ).first()

def get_user_from_userobject(app: App, user: User)-> User:
    return app.query(User).filter(
        and_(
            User.name == user.name, 
            User.role_id == user.role_id
            )
        ).first()
