from flask import *
from flask_sqlalchemy import *

app=Flask(__name__)
app.config.from_pyfile("config.py")
db=SQLAlchemy(app)
