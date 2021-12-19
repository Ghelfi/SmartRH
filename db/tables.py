from app import my_app
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = my_app.db

class Candidat(db.Model):
    __tablename__ = "candidats"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(40), unique=False, nullable=True, index=True)
    user_firstname = db.Column(db.String(40), unique=False, nullable=True)
    phone_number = db.Column(db.String(15), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return (
            f"<Candidat(id={self.id}, "
            f"user_name={self.user_name}, "
            f"user_firstname={self.user_firstname}, "
            f"phone_number={self.phone_number}, "
            f"email={self.email}, "
            f")>"
        )

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True, nullable=False)
    role_value = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return (
            f"<Role(id={self.id}, "
            f"role_name={self.role_name}, "
            f"role_value={self.role_value}, "
            f")>"
        )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', backref="roles")

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name={self.name}, "
            f"role={self.role.role_name}, "
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
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)   

    register = db.relationship('User', backref="users")
    status = db.relationship('Status', backref="status")

    def __repr__(self):
        return (
            f"<CV(id={self.id}, "
            f"filename={self.user_name}, "
            f"date_submission={self.user_firstname}, "
            f"register_by={self.regsiter.name}, "
            f"status={self.status.name}, "
            f")>"
        )

class ExtractionAlgorithm(db.Model):
    __tablename__ = 'algorithms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
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

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cvs.id'), nullable=False)
    algo_id = db.Column(db.Integer, db.ForeignKey('algorithms.id'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)
    value = db.Column(db.String(50), unique=False, nullable=False, index=True)
   
    cv = db.relationship('CV', backref="cvs")
    algo = db.relationship('ExtractionAlgorithm', backref="algorithms")
    field = db.relationship('Field', backref="fields")

    def __repr__(self):
        return (
            f"<Event(id={self.id}, "
            f"cv_filename={self.cv.filename}, "
            f"type={self.field.name}, "
            f"value={self.value}, "
            f"extraction_algorithm={self.algo.name} v{self.algo.version}, "
            f")>"
        )

class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    event_id_one = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event_id_two = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    event_one = db.relationship("Event", foreign_keys=[event_id_one])
    event_two = db.relationship("Event", foreign_keys=[event_id_two])