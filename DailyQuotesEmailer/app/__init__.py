from flask import Flask

app = Flask(__name__)
# secret key given using terminal command: os.urandom(12).hex()
app.config['SECRET_KEY'] = '78414504bd9a44d4de071e39'

from app import routes
