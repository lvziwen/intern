#! coding: utf8
import os

__author__ = 'lvziwen'
import time
from flask import Flask, url_for, render_template
from flask import request, redirect, session
from modules import Student, Session, Enterprise, PhoneKey
import simplejson as json
from tools import get_uid_by_token, make_error, create_token


app = Flask(__name__)
app.config['PROFILE_FOLDER'] = "static/profile"
db_session = Session()
ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
    db_session.add(student)
    db_session.commit()

    phone_key = PhoneKey(id=phone, user_id=student.id)
    db_session.add(phone_key)
    db_session.commit()

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

    student = db_session.query(Student).filter(Student.id==user_id).one()
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
    db_session.add(student)
    db_session.commit()

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
    db_session.add(enterprise)
    db_session.commit()

    result['s'] = 1
    result['m'] = "企业注册成功"
    return json.dumps(result)


@app.route("/student/sign_in")
def sign_in():
    if request.method == "GET":
        parm_dict = request.args
    elif request.method == "POST":
        parm_dict = request.form

    phone = parm_dict.get("phone")
    password = parm_dict.get("password")

    result = dict()
    if not phone or not password:
        return make_error(result, 0, "参数错误")

    phone_key = db_session.query(PhoneKey).filter(id=phone).one()
    if not phone_key:
        return make_error(result, 0, "未注册")

    user_id = phone_key.user_id
    student = db_session.query(Student).filter(id=user_id).one()

    token = create_token()
    session['token_of_phone_' + phone] = token
    session['user_of_token_' + token] = student.id

    result['token'] = token
    user_info = {"id": student.id, "gender": student.gender, "age": student.age, "school": student.school,
                 "academy": student.academy, "major": student.major, "email": student.email, "phone": student.phone}
    result['user_info'] = user_info
    make_error(result, 1, "登陆成功")

    return json.dumps(result)


@app.route("/profile/upload")
def profile_upload():
    if request.method == "GET":
        return "Wrong method"
    elif request.method == "POST":
        parm_dict = request.form

    result = dict()
    token = parm_dict.get()
    user_id = get_uid_by_token(token)
    if not user_id:
        return make_error(result, 0, "登陆错误")
    student = db_session.query(Student).filter(id=user_id).one()
    if not student:
        return make_error(result, 0, "未注册")

    file_obj = request.files['file']
    if file_obj and allowed_file(file_obj.filename):
        filename = str(student.name) + "." + file_obj.filename.rsplit('.', 1)[1]
        file_obj.save(os.path.join(app.config['PROFILE_FOLDER'], filename))

    return make_error(result, 1, "上传简历成功")
