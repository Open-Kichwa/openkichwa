from enum import Enum
from datetime import datetime
from flask_login import UserMixin

from .. import db, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    access_code_id = db.Column(db.Integer, db.ForeignKey("codes.id"), nullable=True)
    community = db.Column(db.String, nullable=False)

    def __init__(self, email, password, community, name=None, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.name = name
        self.is_admin = is_admin
        self.community = community



    def __repr__(self):
        return f"<email {self.email}>"

class AccessCodeTypes(Enum):
    UKN = 0
    BETA = 1

from secrets import choice
from string import ascii_uppercase, digits
def generate_access_code(length=15):
    alphabet = ascii_uppercase + digits
    return "".join(choice(alphabet) for _ in range(length))

class AccessCode(db.Model):
    __tablename__ = "codes"

    id = db.Column(db.Integer, primary_key=True)
    ctype = db.Column(db.Enum(AccessCodeTypes), nullable=False, default=AccessCodeTypes.UKN)
    code = db.Column(db.String(15), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    created_for = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    claimed = db.Column(db.Boolean, nullable=False, default=False)
    claimed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, ctype, created_for=None):
        self.ctype = ctype
        self.created_for = created_for
        self.created_on = datetime.now()
        self.code = generate_access_code()

    def __repr__(self):
        return f"<id {self.id}, code {self.code}>"


        

