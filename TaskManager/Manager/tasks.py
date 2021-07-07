from Manager import db


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    taskTitle = db.Column(db.String(length=1024), nullable=False)
    taskDescription = db.Column(db.String(length=1024), nullable=False)
    dueDate = db.Column(db.Date(), nullable=False)
    dueTime = db.Column(db.Time(), nullable=False)
    color = db.Column(db.String(length=1024), nullable=False)
