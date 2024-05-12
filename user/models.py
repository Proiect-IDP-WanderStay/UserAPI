from dataclasses import dataclass
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

from . import db

@dataclass
class User(db.Model):
   __tablename__ = "Users"

   id: int
   name: str
   password: str
   created_date: datetime
   mail: str

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   name = db.Column(db.String(128), nullable=False)
   password = db.Column(db.String(250), nullable=False)
   created_date = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.utcnow())
   mail = db.Column(db.String(128), nullable=False)

   def __init__(self, id, name, password, created_date, mail):

      self.id = id
      self.name = name
      self.password = self.encrypt_password(password)
      self.created_date = created_date
      self.mail = mail

   def encrypt_password(self, password):
      """Encrypt password"""
      return generate_password_hash(password)



