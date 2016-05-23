import time

__author__ = 'lvziwen'
from flask import Flask
from flask import request
from modules import Student, Session
import simplejson as json
app = Flask(__name__)
session = Session()

@app.route("/sign_up")
def sign_up():
    if request.method == "GET":
        parm_dict = request.args
    elif request.method == "POST":
        parm_dict = request.form

    phone = parm_dict.get("phone")
    password = parm_dict.get("password")
    name = parm_dict.get("name")

    result = {}
    if not phone or not password or not name:
        result['s'] = 0
        result['m'] = "参数错误"
        return json.dumps(result)
    now_time = time.time()
    student = Student(phone=phone, sign_up=now_time, password=password, name=name)
    session.add(student)
    session.commit()

    result['s'] = 1
    result['m'] = "注册成功"
    return json.dumps(result)

