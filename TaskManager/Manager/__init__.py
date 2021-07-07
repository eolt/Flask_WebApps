from flask import Flask  # $ export FLASK_APP=hello   export FLASK_ENV=development
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manager.db'
# secret key given using terminal command: os.urandom(12).hex()
app.config['SECRET_KEY'] = '78414504bd9a44d4de071e39'
db = SQLAlchemy(app)

from Manager import routes
