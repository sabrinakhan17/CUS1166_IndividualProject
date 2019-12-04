from flask import render_template, redirect, url_for, Blueprint, Flask, request
from app.main import bp
from app import db, models
from app.main.forms import TaskForm
from app.models import Task, Appointment

# Main route of the applicaitons.
@bp.route('/', methods=['GET','POST'])
def index():
    return render_template("main/index.html")

@bp.route('/appointment', methods=['GET', 'POST'])
def appointment():
    return render_template("main.appointment")

@bp.route('/createappt', methods=['GET', 'POST'])
def appt():
    form = Appointment()

    if form.validate_on_submit():
        appointment = models.Appointment(appt_title=form.title.data, appt_date=form.data.data, start_time=form.time.data, location=form.location.data, add_notes=form.notes.data, customer_Name=form.name.data, customer_email=form.email.data)
        appointment.status = "Created Appointment"
        db.session.add(appointment)
        db.session.commit()
    return render_template("main.createappt", appointment=appointment)

@bp.route('/editappt/<int:appt_id>', methods=['GET', 'POST'])
def edit(appt_id):
    appt = Appointment.query.get(appt_id)
    appts = Appointment.query.filter_by(appt_id=appt_id)
    appts = Appointment.query.all()
    if(request.method == "POST"):
        appt.appt_title = request.form.get("editTitle")
        appt.appt_date = request.form.get("editData")
        appt.start_time = request.form.get("editTime")
        appt.location = request.form.get("editLocation")
        appt.add_notes = request.form.get("add/editnotes")
        appt.customer_Name = request.form.get("editName")
        appt.customer_email = request.form.get("editEmail")
        appt.status = "Edited Appointment"
        return render_template('viewappt.html', appts=appts)
    return render_template('main.editappt', appts=appts)

@bp.route('/deleteappt/<int:appt_id>', methods=['GET', 'POST', 'DELETE'])
def delete(appt_id):
    appt = Appointment.query.filter_by(appt_id=appt_id).first()
    appt.status = "Deleted"
    db.session.delete(appt)
    db.session.commit()
    appts = Appointment.query.all()
    return render_template('viewappt.html', appts=appts)

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
