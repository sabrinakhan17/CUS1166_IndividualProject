#from flask import url_for
from app import db
from datetime import datetime
#from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True)
    task_desc = db.Column(db.String(128), index=True)
    task_status = db.Column(db.String(128))

class Appointment(db.Model):
    __tablename__ = "Appointment"
    appt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appt_title = db.Column(db.String, nullable=False)
    appt_datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String, nullable=False)
    add_notes = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    customer_Name = db.Column(db.String, nullable=False)
    customer_email = db.Column(db.String, nullable=False)
