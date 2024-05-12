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



@dataclass
class Reservation(db.Model):
   __tablename__ = "Reservations"

   id: int
   user_id: int
   start_date: datetime
   end_date: datetime
   room_id = int 

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   user_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
   start_date = db.Column(db.DateTime, default=0)
   end_date = db.Column(db.DateTime, nullable=False)
   room_id = db.Column(db.Integer, db.ForeignKey("Rooms.id"))

   def __init__(self, user_id, start_date, end_date, room_id):
      self.user_id = user_id
      self.start_date = start_date
      self.end_date = end_date
      self.room_id = room_id



@dataclass
class Room(db.Model):
   __tablename__ = "Rooms"

   id: int
   hotel_id: int
   price: float
   nr_people: int

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   hotel_id = db.Column(db.Integer, db.ForeignKey("Hotels.id"), nullable=False)
   price = db.Column(db.Float(precision=5), nullable=False)
   nr_people = db.Column(db.Integer, nullable=False)
   
   def __init__(self, id, hotel_id, price, nr_people):
      self.id = id
      self.hotel_id = hotel_id
      self.price = price
      self.nr_people = nr_people


@dataclass
class Hotel(db.Model):
   __tablename__ = "Hotels"

   id: int
   name: str
   contact_id: int
   rating: float


   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   name = db.Column(db.String(128), nullable=False)
   contact_id = db.Column(db.Integer, db.ForeignKey("Contact.id"), unique=False)
   rating= db.Column(db.Float(precision=5), unique=False)

   
   def __init__(self, id, name, contact_id, rating):
      self.id = id
      self.name = name
      self.contact_id = contact_id
      self.rating = rating



@dataclass
class Contact(db.Model):
   __tablename__ = "Contact"

   id: int
   phone: str
   country: str
   city: str
   street: str
   email: str

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   phone = db.Column(db.String(128), nullable=False)
   country = db.Column(db.String(128), nullable=False)
   city = db.Column(db.String(128), nullable=False)
   street = db.Column(db.String(128), nullable=False)
   email = db.Column(db.String(128), nullable=False)
   
   def __init__(self, id, phone, country, city, street, email):
      self.id = id
      self.phone = phone
      self.country = country
      self.city = city
      self.street = street
      self.email = email

