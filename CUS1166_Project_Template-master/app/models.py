#from flask import url_for
from app import db
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
    appt_date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    add_notes = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    customer_Name = db.Column(db.String, nullable=False)
    customer_email = db.Column(db.String, nullable=False)
    #CustomerID = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'), nullable=False)

    #customer = db.Relationship("Customer", uselist=False, backref='Appointment')

    def addAppt(self):
        new_appt = Appointment(appt_title=self.appt_title, appt_date=self.appt_date, start_time=self.start_time, location=self.location, add_notes=self.add_notes, customer_Name=self.customer_Name, customer_email=self.customer_email)
        db.session.add(new_appt)
        db.session.commit()

#class Customer(db.Model):
    #__tablename__ = "Customer"
    #customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #customer_Name = db.Column(db.String, nullable=False)
    #customer_email = db.Column(db.String, nullable=False)
    #customer_address = db.Column(db.String, nullable=False)
    #appt_info = db.Column(db.Integer, db.ForeignKey('Appointment.appt_id'), nullable=False)

    #appointment = db.Relationship("Appointment", uselist=False, backref='Customer')
