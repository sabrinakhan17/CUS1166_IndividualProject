
# import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, Email

class TaskForm(FlaskForm):
    task_desc = StringField('task_desc', validators=[DataRequired()])
    task_status_completed = SelectField('Status', choices=[('todo','Todo'),('doing','Doing'),('done','Done')])
    submit = SubmitField('submit')

class Appointment(FlaskForm):
    title = SelectField('Appointment Type', choices=[('Fixing AC Unit', 'Fixing AC Unit'),('Billing', 'Billing'),('Other','Other')])
    date = StringField('Date', validators=[DateField(), DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    name = StringField('Customer Name', validators=[DataRequired(), Length(3, max=45, message='None')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    notes = StringField('Any other notes?')
    submit = SubmitField('submit')

    def validate_email(self, email):
        super()
        appointment = Appointment.query.filter_by(customer_email=email.data).first()
        if appointment is not None:
            raise ValidationError('This email has been taken')
