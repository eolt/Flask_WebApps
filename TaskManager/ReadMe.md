# TaskManager 
## Intro
This is a simple task manager program for the web browser using Flask framework. The user can view tasks specifically due today, tomorrow, or later. 

The tasks due later can range from any point of time in the future. The tasks can be color coded and are specified by date, time, and description. 

The program will save tasks in a local database. And the tasks are displayed in their respective places in order of date or time. The user can modify or delete by simply clicking the button near a task. A task that is not deleted after the due date will be labeled 'overdue' and continues to display on today page; in the case the user hasn't done the task yet.

## Implementation 
The program fulfills the duties for database management using Flask package: SQLAlchemy. Certain routes from flask will handle either adding a task, deleting, modifying, or display. And execute the respective SQL commands for the given action. The program implements the feature FlaskForm, when creating or modifying tasks, for post requests and labeling. A task is represented as an SQL table with a unique ID and set of attributes. A local db file has to be created and assigned before starting the program. This current repository's db file is new and empty, allowing anyone to use this program and run as they please.



