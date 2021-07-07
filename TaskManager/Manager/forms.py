from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    taskTitle = StringField(label="Task Tile:", validators=[DataRequired()])
    taskDescription = StringField(label="Task Description:", validators=[DataRequired()])
    dueDate = DateField(label="Due Date:", format="%Y-%m-%d", validators=[DataRequired()])
    dueTime = TimeField(label="Time Due:", validators=[DataRequired()])
    color = StringField(label="Color:", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

