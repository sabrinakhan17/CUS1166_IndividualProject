import datetime
from flask import render_template, redirect, url_for, request, flash
from app.main import *
from app.main import bp
from sqlalchemy.testing import db
from app.models import *
from app.models import Task
from app.models import Appointment
from .forms import TaskForm, AppointmentF

# Main route of the applicaitons.
@bp.route('/', methods=['GET','POST'])
def index():
    return render_template("main/index.html")

@bp.route('/appointment', methods=['GET', 'POST'])
def appointment():
    return render_template("main/appointment.html")

@bp.route('/createappt', methods=['GET', 'POST'])
def appt():
    form = Appointment()

    if form.validate_on_submit():
        appts = AppointmentF()
        appts.appt_title=form.title.data
        appts.appt_datetime=datetime.datetime.combine(form.date.data, form.time.data)
        appts.location=form.location.data
        appts.add_notes=form.notes.data
        appts.customer_Name=form.name.data
        appts.customer_email=form.email.data
        appts.appointment.status = "Created Appointment"
        db.session.add(appts)
        db.session.commit()
        flash('Successfully created the appointment!', category='success')
    return render_template("main/createappt.html", appts=appts, form=form)

@bp.route('/editappt/<int:appt_id>', methods=['GET', 'POST'])
def edit(appt_id):
    form = AppointmentF()
    appt = Appointment.query.get(appt_id)
    if(request.method == "POST"):
        appt.appt_title = form.title.data
        appt.appt_datetime = datetime.datetime.combine(form.date.data, form.time.data)
        appt.location = form.location.data
        appt.add_notes = form.notes.data
        appt.customer_Name = form.name.data
        appt.customer_email = form.email.data
        appt.status = "Edited Appointment"
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('viewappt.html', appt=appt))
    return render_template("main/editappt.html", form=form, appt=appt)

@bp.route('/deleteappt/<int:appt_id>', methods=['GET', 'POST', 'DELETE'])
def delete(appt_id):
    appt = Appointment.query.get(appt_id)
    appt.status = "Deleted"
    db.session.delete(appt)
    db.session.commit()
    flash('Successfully deleted appointment!', category='success')
    return render_template("main/viewappt.html")

@bp.route('/apptview', methods=['GET', 'POST'])
def apptview():
    appts = Appointment.query.all()
    return render_template("main/viewappt.html", appts=appts)

#
#  Route for viewing and adding new tasks.
@bp.route('/todolist', methods=['GET','POST'])
def todolist():
    form = TaskForm()

    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.
        new_task = Task()
        new_task.task_desc =  form.task_desc.data
        new_task.task_status = form.task_status_completed.data

        db.session.add(new_task)
        db.session.commit()

        # Redirect to this handler - but without form submitted - gets a clear form.
        return redirect(url_for('main.todolist'))

    todo_list = db.session.query(Task).all()

    return render_template("main/todolist.html",todo_list = todo_list,form= form)


#
# Route for removing a task
@bp.route('/todolist/remove/<int:task_id>', methods=['GET','POST'])
def remove_task(task_id):

    # Query database, remove items
    Task.query.filter(Task.task_id == task_id).delete()
    db.session.commit()

    return redirect(url_for('main.todolist'))


#
# Route for editing a task

@bp.route('/todolist/edit/<int:task_id>', methods=['GET','POST'])
def edit_task(task_id):
    form = TaskForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        # Get the data from the form, and add it to the database.

        current_task = Task.query.filter_by(task_id=task_id).first_or_404()
        current_task.task_desc =  form.task_desc.data
        current_task.task_status = form.task_status_completed.data

        db.session.add(current_task)
        db.session.commit()
        # After editing, redirect to the view page.
        return redirect(url_for('main.todolist'))

    # get task for the database.
    current_task = Task.query.filter_by(task_id=task_id).first_or_404()

    # update the form model in order to populate the html form.
    form.task_desc.data =     current_task.task_desc
    form.task_status_completed.data = current_task.task_status

    return render_template("main/todolist_edit_view.html",form=form, task_id = task_id)
