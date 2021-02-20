from flask import Flask, render_template, url_for, flash, redirect,request,session,Response,jsonify
from forms import RegistrationForm, LoginForm, ChangePasswordForm, RequestResetForm,ResetPasswordForm, ExamInfoForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from countdown import countdown
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import login_user, current_user, logout_user, login_required
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_restful import Resource, Api, reqparse
from flask_mail import Message
from datetime import date
import smtplib
import os
import secrets
import json
from flask_cors import CORS
from pusher import pusher
import simplejson
import cv2


app = Flask(__name__)
camera = cv2.VideoCapture(0)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://kmehjunwelbxem:3a5bd15721c4b183a610f35e1228e8c3cfb1173010a07d43f7d215dde7f03b20@ec2-3-210-23-22.compute-1.amazonaws.com:5432/d33g4onqiumn8h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
pusher = pusher.Pusher(app_id = "1134388", key = "a60f02f7bde182f427ce", secret = "f42daac6390680efc75f", cluster = "ap2", ssl=True)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
parser = reqparse.RequestParser()
class UserInformation( db.Model,UserMixin):
    __tablename__ = 'App_students'

    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String())
    student_email = db.Column(db.Text())
    student_phone = db.Column(db.Integer)
    session = db.Column(db.Integer)
    student_address = db.Column(db.Text())
    country = db.Column(db.Text())
    state = db.Column(db.Text())
    city = db.Column(db.Text())
    section = db.Column(db.Text())
    student_password = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    branch_id_id = db.Column(db.Integer)
    college_id_id = db.Column(db.Integer)
    semester_id_id = db.Column(db.Integer)


class CollegeInfo( db.Model,UserMixin):
    __tablename__ = 'App_college'

    user_id_id = db.Column(db.Integer, primary_key=True)
    college_name = db.Column(db.String())
    college_code = db.Column(db.Text())
    college_address = db.Column(db.Text())
    college_university = db.Column(db.String())
    college_contact = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id = db.Column(db.Integer)

class ProctorInfo( db.Model,UserMixin):
    __tablename__ = 'App_proctor'

    proctor_id = db.Column(db.Integer, primary_key=True)
    proctor_name = db.Column(db.String())
    proctor_email = db.Column(db.Text())
    proctor_phone = db.Column(db.Integer)
    proctor_password = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id_id = db.Column(db.Integer)
    assign_section=db.Column(db.Text())

class CollegeExam( db.Model,UserMixin):
    __tablename__ = 'App_exam'

    exam_id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String())
    instructions = db.Column(db.Text())
    duration = db.Column(db.Text())
    date = db.Column(db.Text())
    starting_time = db.Column(db.Text())
    ending_time = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id_id = db.Column(db.Integer)
    subject_id_id = db.Column(db.Integer)
    semester_id_id = db.Column(db.Integer)
    branch_id_id = db.Column(db.Integer)


class BranchInfo( db.Model,UserMixin):
    __tablename__ = 'App_branch'
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    college_id_id = db.Column(db.Integer)

class SubjectInfo( db.Model,UserMixin):
    __tablename__ = 'App_subject'
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String())
    subject_code = db.Column(db.String())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    total_marks = db.Column(db.Integer)
    college_id_id = db.Column(db.Integer)
    branch_id_id = db.Column(db.Integer)




class QuestionInfo( db.Model,UserMixin):
    __tablename__ = 'App_questions'

    question_id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(db.String())
    option_a = db.Column(db.Text())
    option_b = db.Column(db.Text())
    option_c = db.Column(db.Text())
    option_d = db.Column(db.Text())
    answer = db.Column(db.Text())
    section = db.Column(db.Text())
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    marks = db.Column(db.Integer)
    branch_id_id = db.Column(db.Integer)
    college_id_id = db.Column(db.Integer)
    exam_id_id = db.Column(db.Integer)
    subject_id_id = db.Column(db.Integer)


class AnswerInfo( db.Model,UserMixin):
    __tablename__ = 'App_answer'

    answer_id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text())
    
    doc = db.Column(db.Text())
    slug = db.Column(db.Text())
    question_id_id = db.Column(db.Integer)
    student_id_id = db.Column(db.Integer)
    exam_id_id = db.Column(db.Integer)

def load_user(user_pk):
   return g.session.query(UserInformation).get(user_pk)

@app.route('/',methods=["GET","POST"])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        registeredUser = UserInformation.query.filter_by(student_email=email,student_password=password).first()
        ProctorUser = ProctorInfo.query.filter_by(proctor_email=email,proctor_password=password).first()
        
        
        try:
      #student a particular proctor is assigned
            college_details = CollegeInfo.query.filter_by(college_id=ProctorUser.college_id_id).first()
            section1 = UserInformation.query.filter_by(section=ProctorUser.assign_section).all()
            sections = []
            for index, i in enumerate(section1):
                q_info = i.student_email
                sections.append(q_info)
            # print(sections)
            # res = [] 
            # for idx, sub in enumerate(sections, start = 0): 
            #         res.append(list(sub)) 
            # # input list 
            # l = res
            # output = [] 
            # def reemovNestings(l): 
            #     for i in l: 
            #         if type(i) == list: 
            #             reemovNestings(i) 
            #         else: 
            #             output.append(i) 
            # reemovNestings(l)     
            # print(output)
        except:
            print("student signed in...")

        try:
            # print("yha hu")
            signin.name=registeredUser.student_name
            signin.email=registeredUser.student_email
            signin.student_id=registeredUser.student_id
            signin.college_id=registeredUser.college_id_id
            signin.semester_id_id=registeredUser.semester_id_id
            signin.branch_id_id=registeredUser.branch_id_id
            exam_details = CollegeExam.query.filter_by(college_id_id=signin.college_id,semester_id_id=signin.semester_id_id,branch_id_id=signin.branch_id_id).first()
            AnswerUser = AnswerInfo.query.filter_by(student_id_id=signin.student_id,exam_id_id=exam_details.exam_id).first()
            # print("ye hai exam")
        except:
            print("something went wrong")
        if registeredUser is not None and AnswerUser is None :
            from datetime import date
            today = date.today()   
            print('Logged in..')
            session['logged_in']=True
            session['user_id'] = signin.student_id
            today = date.today()  
            college_details = CollegeInfo.query.filter_by(college_id=signin.college_id).first()
            exam_details = CollegeExam.query.filter_by(college_id_id=signin.college_id,semester_id_id=signin.semester_id_id,branch_id_id=signin.branch_id_id,date=today).first()
            exam_details = CollegeExam.query.filter_by(college_id_id=signin.college_id,semester_id_id=signin.semester_id_id,branch_id_id=signin.branch_id_id,date=today).first()
            print("exam time",college_details.college_university)
        
            try:
                signin.duration_exam=exam_details.duration
                from datetime import datetime
                now = datetime.now()
                now=now.strftime("%H:%M")
                start = exam_details.starting_time
                end1 = exam_details.ending_time
                new=datetime.strptime(start,"%H:%M")
                new=new.strftime("%H:%M")
                old=datetime.strptime(end1,"%H:%M")
                old=old.strftime("%H:%M")
                signin.exam_id=exam_details.exam_id
            except:
                msg="Today no exam available for you!!"
                return render_template('base.html',msg=msg)
            return render_template('student.html',registeredUser=registeredUser,exam_details=exam_details,college_details=college_details,new=new,old=old,now=now)
        elif ProctorUser is not None:
            return render_template('proctor.html',proctorname=ProctorUser.proctor_name,college_name=college_details.college_university,sections=sections)
        try:
            if AnswerUser is not None:
                msg='You already attempted the test'
                return render_template('base.html',msg=msg)
            else:
                msg='No exam has been assigned to u...'
                return render_template('base.html',msg=msg)
        except:
            msg='Invalid Credentials!!!'
            return render_template('base.html',msg=msg)       
        
    else:
        return render_template('base.html')
        # return 'all okay'

# from cryptography.fernet import Fernet
# key = Fernet.generate_key() #this is your "password"
# cipher_suite = Fernet(key)
# encoded_text = cipher_suite.encrypt(b"test")
# encoded_text=encoded_text[3:20]

@app.route('/calculator',methods=["GET","POST"])
def calc():
    return render_template("calculator.html")
 
@app.route('/test',methods=["GET","POST"])
def test():
    return render_template('quizJS.html', user_id=signin.student_id, stu_name=signin.name,duration_exam=signin.duration_exam,student_email=signin.email)

@app.route('/new/guest', methods=['POST'])
def guestUser():
    data = request.json
    pusher.trigger(u'general-channel', u'new-guest-details', { 
        'name' : data['name'], 
        'email' : data['email']
        })
    return json.dumps(data)

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
    auth = pusher.authenticate(channel=request.form['channel_name'],socket_id=request.form['socket_id'])
    return json.dumps(auth)

class QuestionSubmit(Resource):
    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        student_id = data['user_id']
        value = data['ans']
        import pandas as pd
        from pandas import DataFrame
        df1=list(value.values())
        df2=list(value.keys())
        df3=[df1,df2]
        # print(df3)
        exam_details = CollegeExam.query.filter_by(college_id_id=signin.college_id,semester_id_id=signin.semester_id_id,branch_id_id=signin.branch_id_id).first()
        df = DataFrame (df3,['answer','question_id_id']).transpose()
        df['student_id_id']=student_id
        df['exam_id_id']=exam_details.exam_id
        df['doc']='2021-01-16T22:23:31.000+00:00'
        df['slug']='memory-leak-2021-01-17-0353310530'

        
        # print(df)
        import sqlalchemy 
        engine=sqlalchemy.create_engine('postgres://kmehjunwelbxem:3a5bd15721c4b183a610f35e1228e8c3cfb1173010a07d43f7d215dde7f03b20@ec2-3-210-23-22.compute-1.amazonaws.com:5432/d33g4onqiumn8h')
        con=engine.connect()
        table_name='App_answer'
        df.to_sql(table_name,con,if_exists='append',index=False)
        con.close()
        return({'message':'Test Submitted Successfully'})

class QuestionList(Resource):

    def post(self):
        data = request.data.decode('UTF-8')
        data = json.loads(data)
        # print(data)
        student_id = data['user_id']
        # print(student_id)
        question = []
        # print(current_user)
        student = UserInformation.query.filter_by(student_id=student_id).first()
        question = QuestionInfo.query.filter_by(college_id_id=student.college_id_id,exam_id_id=signin.exam_id).all()
        # print( "ye hai questions",question)
        questions = []
        for index, i in enumerate(question):
            q_info = {}
            q_info['question_id'] = i.question_id
            q_info['question'] = i.questions
            q_info['option_a'] = i.option_a
            q_info['option_b'] = i.option_b
            q_info['option_c'] = i.option_c
            q_info['option_d'] = i.option_d
            questions.append(q_info)
        return questions

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


api.add_resource(QuestionList, '/question-list')
api.add_resource(QuestionSubmit, '/submit-test')


if __name__ == "__main__":
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return None
    login_manager.login_view = 'login'
    app.run(debug=True)
