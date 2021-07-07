from flask import Flask  # $ export FLASK_APP=hello   export FLASK_ENV=development

app = Flask(__name__)
# secret key given using terminal command: os.urandom(12).hex()
app.config['SECRET_KEY'] = '78414504bd9a44d4de071e39'

from quiz import routes
