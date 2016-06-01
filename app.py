#! coding: utf8
__author__ = 'lvziwen'
import time
from flask import Flask
from flask import request
from modules import Student, Session, Enterprise
import simplejson as json
from tools import get_uid_by_token
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


@app.route("/user/info_add")
def user_info_add():
    if request.method == "GET":
        parm_dict = request.args
    elif request.method == "POST":
        parm_dict = request.form

    school = parm_dict.get("school")
    academy = parm_dict.get("academy")
    major = parm_dict.get("major")
    age = parm_dict.get("age")
    gender = parm_dict.get("gender")
    email = parm_dict.get("email")
    qq = parm_dict.get("qq")
    token = parm_dict.get("token")

    result = {}
    user_id = get_uid_by_token(token)
    if not user_id:
        result['s'] = 0
        result['m'] = "登录过期，请重新登录"
        return json.dumps(result)

    student = session.query(Student).filter(Student.id==user_id).one()
    if not student:
        result['s'] = 0
        result['m'] = "帐号不存在"
        return json.dumps(result)

    student.school = school
    student.academy = academy
    student.major = major
    student.age = age
    student.gender = gender
    student.email = email
    student.qq_num = qq
    session.add(student)
    session.commit()

    result['s'] = 1
    result['m'] = "更新用户信息成功"
    return json.dumps(result)


@app.route("/enterprise/sign_up")
def enterprise_sign_up():
    if request.method == "GET":
        parm_dict = request.args
    elif request.method == "POST":
        parm_dict = request.form

    result = {}

    name = parm_dict.get("name")
    industry = parm_dict.get("industry")
    description = parm_dict.get("description")
    email = parm_dict.get("email")

    if not name or not industry or not description:
        result['s'] = 0
        result['m'] = "参数错误"
        return json.dumps(result)
    now = int(time.time())
    enterprise = Enterprise(name=name, industry=industry, description=description, sign_up_time=now, update_time=now,
                            email=email)
    session.add(enterprise)
    session.commit()

    result['s'] = 1
    result['m'] = "企业注册成功"
    return json.dumps(result)