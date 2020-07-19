from flask import *
from flask_sqlalchemy import *
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

# 允许跨域
CORS(app, supports_credentials=True)

import time
from datetime import timedelta

from celery import Celery

# # 创建celery对象,设置任务队列使用redis
# broker = 'redis://0.0.0.0:6379/0'
# backend = 'redis://0.0.0.0:6379/1'
# celery = Celery('test',broker=broker, backend=backend,
#     #包含以下链各个任务文件，去响应的py文件中找任务，对多个任务做分类
#     include=['tasks',])
