from flask import *
from flask_sqlalchemy import *
from flask_cors import CORS
app=Flask(__name__)
app.config.from_pyfile("config.py")
db=SQLAlchemy(app)

CORS(app, supports_credentials=True)