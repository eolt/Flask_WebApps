from flask import render_template, redirect, url_for, flash, request
from Manager import app, db
from Manager.forms import TaskForm
from Manager.tasks import Task
from datetime import date, timedelta


@app.route('/')
def main_page():
    return redirect(url_for('task_page', day=0))


@app.route('/task/<day>', methods=['GET', 'POST'])
def task_page(day):
    if request.method == 'POST':

        req = request.form.to_dict()

        task_id = next((iter(req)))

        if req[task_id] == 'Modify':
            return redirect(url_for('handle_modify', task_id=task_id))
        elif req[task_id] == 'Delete':
            task_to_delete = Task.query.filter_by(id=task_id).one()

            db.session.delete(task_to_delete)
            db.session.commit()

        return redirect(url_for('task_page', day=day))

    if request.method == 'GET':
        later = False

        if day == '0':
            tasks = Task.query.filter(Task.dueDate <= date.today()).order_by(Task.dueTime)
        elif day == '1':
            tasks = Task.query.filter_by(dueDate=(date.today() + timedelta(days=1))).order_by(Task.dueTime)
        else:
            tasks = Task.query.filter(Task.dueDate > (date.today() + timedelta(days=1))).order_by(Task.dueDate)
            later = True

        if tasks.count() == 0:
            return render_template('home.html', msg='There are no tasks display.')
        else:
            return render_template('displayTasks.html', tasks=tasks, isLater=later, currDay=date.today())


@app.route('/add', methods=['GET', 'POST'])
def add_task_page():
    form = TaskForm()

    if request.method == 'POST':
        task_to_create = Task(
            taskTitle=form.taskTitle.data,
            taskDescription=form.taskDescription.data,
            dueDate=form.dueDate.data,
            dueTime=form.dueTime.data,
            color=form.color.data
        )

        db.session.add(task_to_create)
        db.session.commit()
        return redirect(url_for('task_page', day=0))

    if form.errors != {}:  # no errors from the validations
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template('addTaskForm.html', form=form)


@app.route('/modify/<task_id>', methods=['GET', 'POST'])
def handle_modify(task_id):
    task_to_modify = Task.query.filter_by(id=task_id).one()

    form = TaskForm()

    if request.method == 'POST':

        task_to_modify = Task.query.filter_by(id=task_id).one()

        task_to_modify.taskTitle = form.taskTitle.data
        task_to_modify.taskDescription = form.taskDescription.data
        task_to_modify.dueDate = form.dueDate.data

        if form.dueTime.data is not None:
            task_to_modify.dueTime = form.dueTime.data

        task_to_modify.color = form.color.data

        db.session.commit()

        return redirect(url_for('task_page', day=0))

    if form.errors != {}:  # no errors from the validations
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template('modifyTaskForm.html', form=form, task=task_to_modify)
