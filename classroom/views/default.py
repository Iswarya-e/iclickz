from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from sklearn.feature_extraction.text import TfidfTransformer
import nltk,string, numpy
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import update
import transaction
from sqlalchemy import func
import csv
import datetime
from sqlalchemy.exc import DBAPIError
import os
from datetime import time
import pyramid_excel as excel
import base64
import codecs
from pyramid.httpexceptions import HTTPFound
import zipfile as Z
from pyramid.response import Response
import psycopg2
import uuid
import shutil



import requests
from ..models import MyModel
from ..models import Student
from ..models import Teacher
from ..models import Course
from ..models import Test
from ..models import DescQuestion
from ..models import Mcq
from ..models import Mcqn
from ..models import Truefalse
from ..models import Studentcourse
from ..models import StudentDescmark
from ..models import Studentflip
from ..models import Studentattendance
from ..models import Studenttfmark
from ..models import Studentmcqmark
from ..models import Quiz
from ..models import Quizquestion
from ..models import Studentquiz
from ..models import Forum
from ..models import Comments
import re
currentDT = datetime.date.today()
@view_config(route_name='veryfirst', renderer='../templates/veryfirstjinja2')
def first(request):
    try:
        session = request.session

        return render_to_response('../templates/veryfirst.jinja2',{},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studentlogin', renderer='../templates/studentlogin.jinja2')
def student(request):
    try:
        session = request.session
        return render_to_response('../templates/studentlogin.jinja2',{},request=request)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='teacherprofile', renderer='../templates/teacherprofile.jinja2')
@view_config(route_name='tp')
def tprof(request):
    try:
        session =request.session
        email = session['usermail']
        password = session['pwd']
        tabledata = request.dbsession.query(Teacher)

        name = tabledata.filter((Teacher.email_id == email) & (Teacher.password == password)).all()
        for i in name:
            username = i.username
            insname = i.institute_name
            email1 = i.email_id
            id = i.teacher_id
        return render_to_response('../templates/teacherprofile.jinja2',{ 'session' : session ,'name' : username ,'ins' : insname, 'email' : email1},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='teacheredit')
def tprof1(request):
    try:
        session =request.session
        email = session['usermail']
        tabledata = request.dbsession.query(Teacher)
        password = session['pwd']
        name = tabledata.filter((Teacher.email_id == email) & (Teacher.password == password)).all()
        for i in name:
            username = i.username
            insname = i.institute_name
            email1 = i.email_id
            id = i.teacher_id

        return render_to_response('../templates/teachereditprofile.jinja2',{ 'session' : session ,'name' : username ,'ins' : insname, 'email' : email1 ,'id' : id},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
@view_config(route_name='teditsuccess')
def teditsuccess(request):
    try:
        session =request.session
        email = session['usermail']
        tabledata = request.dbsession.query(Teacher)
        password = session['pwd']
        name = tabledata.filter(Teacher.teacher_id == session['tid']).all()
        for i in name :

            tabname = i.username
            tabpass = i.password
            tabmail = i.email_id
            tabins = i.institute_name

        username = request.params['name']
        insname = request.params['insname']
        pwd = request.params['pwd']
        id =  request.params['email']
        request.dbsession.query(Teacher).filter(Teacher.teacher_id == session['tid']).update({Teacher.username:func.replace(Teacher.username,tabname,username)},synchronize_session=False)
        request.dbsession.query(Teacher).filter(Teacher.teacher_id == session['tid']).update({Teacher.password:func.replace(Teacher.password,tabpass,pwd)},synchronize_session=False)
        request.dbsession.query(Teacher).filter(Teacher.teacher_id == session['tid']).update({Teacher.email_id:func.replace(Teacher.email_id,tabmail,id)},synchronize_session=False)
        request.dbsession.query(Teacher).filter(Teacher.teacher_id == session['tid']).update({Teacher.institute_name:func.replace(Teacher.institute_name,tabins,insname)},synchronize_session=False)
        return render_to_response('../templates/teacherprofile.jinja2',{ 'session' : session ,'name' : username ,'ins' : insname, 'email' : id},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='studentprofile', renderer='../templates/studentprofile.jinja2')
@view_config(route_name='sp')
def sprof(request):
    try:
        session = request.session
        email = session['usermail']
        password = session['pwd']
        tabledata = request.dbsession.query(Student)

        name = tabledata.filter(Student.email_id == email and Student.password == password).all()
        for i in name:
            username = i.name
            insname = i.institute_name
            email1 = i.email_id
            id = i.student_id
        return render_to_response('../templates/studentprofile.jinja2',{'session' : session , 'name' : username ,'ins' : insname, 'email' : email1, 'id' : id},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studentedit')
def sprof1(request):
    try:
        session =request.session
        email = session['usermail']
        tabledata = request.dbsession.query(Student)
        password = session['pwd']
        name = tabledata.filter((Student.email_id == email) & (Student.password == password)).all()
        for i in name:
            username = i.name
            insname = i.institute_name
            email1 = i.email_id
            id = i.student_id

        return render_to_response('../templates/studenteditprofile.jinja2',{ 'session' : session ,'name' : username ,'ins' : insname, 'email' : email1 ,'id' : id},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
@view_config(route_name='seditsuccess')
def seditsuccess(request):
    try:
        session =request.session
        email = session['usermail']
        tabledata = request.dbsession.query(Student)
        password = session['pwd']
        name = tabledata.filter(Student.student_id == session['sid']).all()
        for i in name :

            tabname = i.name
            tabpass = i.password
            tabmail = i.email_id
            tabins = i.institute_name

        username = request.params['name']
        insname = request.params['insname']
        pwd = request.params['pwd']
        id =  request.params['email']
        request.dbsession.query(Student).filter(Student.student_id == session['sid']).update({Student.name:func.replace(Student.name,tabname,username)},synchronize_session=False)
        request.dbsession.query(Student).filter(Student.student_id == session['sid']).update({Student.password:func.replace(Student.password,tabpass,pwd)},synchronize_session=False)
        request.dbsession.query(Student).filter(Student.student_id == session['sid']).update({Student.email_id:func.replace(Student.email_id,tabmail,id)},synchronize_session=False)
        request.dbsession.query(Student).filter(Student.student_id == session['sid']).update({Student.institute_name:func.replace(Student.institute_name,tabins,insname)},synchronize_session=False)
        return render_to_response('../templates/studentprofile.jinja2',{ 'session' : session ,'name' : username ,'ins' : insname, 'email' : id},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(accept='text/css',route_name='s2')
def studentlog(request):
    try:
        email = request.params['email']
        password = request.params['pwd']
        tab = request.dbsession.query(Student)

        session = request.session
        session['usermail'] = email
        session['pwd'] = password

        name = tab.filter(Student.email_id == email and Student.password == password).all()
        for i in name:
            if i.email_id == email and i.password == password:
                session['sid'] = i.student_id
                return render_to_response('../templates/studentnav.jinja2',{'session' : session },request=request)
            else:
                return render_to_response('../templates/studentlogin.jinja2',{'session' : session,'error' : 'Enter correct details'},request=request)
    except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='teacherlogin', renderer='../templates/teacherlogin.jinja2')
def teacher(request):
    try:
        session = request.session
        return render_to_response('../templates/teacherlogin.jinja2',{},request=request)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='t2')
def teacherlog(request):
    try:
        email = request.params['email']
        password = request.params['pwd']
        tabledata = request.dbsession.query(Teacher)

        session = request.session
        session['usermail'] = email
        session['pwd'] = password

        name = tabledata.filter(Teacher.email_id == email and Teacher.password == password).all()

        for i in name:

            if i.email_id == email and i.password == password:
                session['tid'] = i.teacher_id
                return render_to_response('../templates/teachernav.jinja2',{'session' : session },request=request)
            else:
                return render_to_response('../templates/teacherlogin.jinja2',{},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='studentnav', renderer='../templates/studentnav.jinja2')
@view_config(route_name='teachernav', renderer='../templates/teachernav.jinja2')


@view_config(route_name='studentsignup', renderer='../templates/studentsignup.jinja2')

def student1(request):
    try:
        session = request.session
        return render_to_response('../templates/studentsignup.jinja2',{},request=request)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='s1')
def s1(request):
   try:
       print("try")
       query1 = request.dbsession.query(Student)
       name = request.params['name']
       Institution_name = request.params['insnm']
       password = request.params['password']
       email = request.params['email']
       rppwd = request.params['rppwd']
       for i in query1:
           if i.email_id == email:
               	  return render_to_response('../templates/studentsignup.jinja2',{'error1' : 'User already exists !'},request=request)
       if re.match(r'[A-Za-z0-9@#$%^&+=]{4,}', password):
                 if rppwd == password:
                   obj = Student()
                   obj.name = name
                   obj.institute_name = Institution_name
                   obj.password = password
                   obj.email_id = email
                   request.dbsession.add(obj)
                   return render_to_response('../templates/studentlogin.jinja2',{},request=request)
                 else:
                   return render_to_response('../templates/studentsignup.jinja2',{'error2' : 'passwords does not match !'},request=request)
       else:
            return render_to_response('../templates/studentsignup.jinja2',{'error3' : 'Password must contain atleast one capital letter,one smmall letter,a number and a special character !'},request=request)
   except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='teachersignup', renderer='../templates/teachersignup.jinja2')
def teacher1(request):
    try:
        session = request.session
        return render_to_response('../templates/teachersignup.jinja2',{},request=request)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='t1')
def t1(request):
   try:
       query1 = request.dbsession.query(Teacher)
       session = request.session
       name = request.params['name']
       Institution_name = request.params['insname']
       password = request.params['pwd']
       email = request.params['email']
       rppwd = request.params['rppwd']

       for i in query1:
            if i.email_id == email:
               	   return render_to_response('../templates/teachersignup.jinja2',{'error1' : 'User already exists !'},request=request)
       if re.match(r'[A-Za-z0-9@#$%^&+=]{4,}', password):
        if rppwd == password:
            obj = Teacher()
            obj.username = name
            obj.institute_name = Institution_name
            obj.password = password
            obj.email_id = email
            request.dbsession.add(obj)
            return render_to_response('../templates/teacherlogin.jinja2',{},request=request)
        else:
          return render_to_response('../templates/teachersignup.jinja2',{'error2' : 'passwords does not match !'},request=request)
       else:
          return render_to_response('../templates/teachersignup.jinja2',{'error3' : 'Password must contain atleast one capital letter,one smmall letter,a number and a special character !'},request=request)
   except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(route_name='nav')
def navi(request):
    try:
        session = request.session
        return render_to_response('../templates/createcourse.jinja2',{'session' : session},request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)


#@view_config(route_name='addcourse', renderer='../templates/addcourse.jinja2')

@view_config(route_name='createcourse', renderer='../templates/createcourse.jinja2')


@view_config(route_name='createcourseform', renderer='../templates/createcourseform.jinja2')
def create(request):
    try:
        session = request.session

        return render_to_response('../templates/createcourseform.jinja2',{'session' : session},request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='c1')
def courseadd(request):
  try:
        query = request.dbsession.query(Course)
        session = request.session
        cname = str(request.params['coursename'])
        domname = request.params['domname']
        cid = request.params['courseid']
        #for i in query:
            #if i.course_id == cid:
        getCourse=request.dbsession.query(Course).filter(Course.course_id==cid).first()
        if(getCourse is not None):
                return render_to_response('../templates/createcourseform.jinja2',{'error' : 'Course ID already taken'}, request=request)
        else:
            obj1 = Course()
            obj1.teacher_id = session['tid']
            obj1.course_id = cid
            obj1.course_name = cname
            obj1.course_discipline = domname
            request.dbsession.add(obj1)
        url=request.route_url('check')
        return HTTPFound(url)
        #return render_to_response('../templates/continuecourse.jinja2',{'session' : session},request=request)

  except DBAPIError:
       return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='check')
def check123(request):
    try:
        print("hello")
        session = request.session
        tid = session['tid']
        tabledata = request.dbsession.query(Course)
        coursedet = tabledata.filter(Course.teacher_id == tid).all()
        print(coursedet)
        return render_to_response('../templates/displaycourse.jinja2',{'session' : session, 'course' : coursedet, },request=request)

    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)








############################################################################################3
#@view_config(route_name='flipdet')
#ef flipdet(request):
#    try:
#        session = request.session
#        tid = session['tid']
#        det = request.dbsession.query(Student).filter(Student.cid ==).first()


###########################################################################################
@view_config(route_name='displaytest', renderer='../templates/displaytest.jinja2')
def disptest(request):
 try:
    session = request.session
    return render_to_response('../templates/displaytest.jinja2',{'session' : session},request=request)

 except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='displaycourse', renderer='../templates/displaycourse.jinja2')


@view_config(route_name='checktest')
def checktest(request):
  try:
    query1 = request.dbsession.query(Test)
    session = request.session
    session['cid'] = request.params['course_id']
    cid = session['cid']
    det = query1.filter(Test.courseid == cid).all()
    id1 = " "
    for i in det:
        id1 = i.test_id

    return render_to_response('../templates/displaytest.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(route_name='ctac')
def testcheck(request):
  try:
    query1 = request.dbsession.query(Test)
    session = request.session
    cid = session['cid']
    det = query1.filter(Test.courseid == cid).all()
    id1 = " "
    for i in det:
        id1 = i.test_id
    return render_to_response('../templates/displaytest.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)
  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)
@view_config(route_name='test', renderer='../templates/test.jinja2')

@view_config(route_name='test1')
def test1(request):
    try:
        session = request.session
        return render_to_response('../templates/test.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='test2')
def test2(request):
    try:
        session = request.session
        query = request.dbsession.query(Test)
        obj = Test()
        obj.test_name = request.params['tname']
        obj.courseid = session['cid']
        obj.questiontype = request.params['qntype']
        obj.start_date = request.params['sdate']
        obj.end_date = request.params['edate']

        request.dbsession.add(obj)
        qtype = request.params['qntype']
        det = query.filter(Test.test_name == request.params['tname']).all()
        session['qtype'] = qtype
        for i in det:
            session['testid'] = i.test_id
        if qtype == "mcq":

            return render_to_response('../templates/mcqteacherinput.jinja2',{'session' : session},request=request)
        if qtype == "mcqn":
            return render_to_response('../templates/mcqnteacherinput.jinja2',{'session' : session},request=request)
        if qtype == "truefalse":
            return render_to_response('../templates/tfteacherinput.jinja2',{'session' : session},request=request)
        if qtype == "openended":
            return render_to_response('../templates/desteacherinput.jinja2',{'session' : session},request=request)


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='desteacherinput', renderer='../templates/desteacherinput.jinja2')






@view_config(route_name='continue')
def conti(request):
  try:
       session = request.dbsession
       return render_to_response('../templates/continue.jinja2',{'session' : session},request=request)
  except DBAPIError:
      return Response(db_err_msg, content_type='text/plain', status=500)


def get_bytes_from_file(filename):
    return open(filename,"rb",buffering=0).read()

@view_config(route_name='des2')
def des2(request):
    try:
        session = request.session

        qn = request.params['qname']
        ans = request.params['qans']
        qno = request.params['qno']
        qmark = request.params['qmark']
        link = request.params['qlink']
        img=request.params['img']

        #image =request.params['img']
        query = request.dbsession.query(DescQuestion)








        obj = DescQuestion()
        obj.Question_name = qn
        obj.Answer = ans
        obj.question_no = qno
        obj.qmark = qmark
        obj.qlink = link
        obj.image = img

        obj.test_id = session['testid']
        request.dbsession.add(obj)
        url=request.route_url('ctac')
        return HTTPFound(url)
        return render_to_response('../templates/continue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='dispques')
def dispques(request):
    try:
        session = request.session
        tid = request.params['test_id']
        session['testid'] = tid
        query = request.dbsession.query(Test)
        det = query.filter(Test.test_id == tid).all()
        for i in det:
            qtype = i.questiontype
        if qtype == "mcq":

            session['qtype'] = qtype
            query = request.dbsession.query(Mcq)
            det = query.filter(Mcq.test_id == session['testid']).all()
            return render_to_response('../templates/mcqdisplayquestion.jinja2',{'session' : session,'det' : det},request=request)
        if qtype == "mcqn":

            session['qtype'] = qtype
            query = request.dbsession.query(Mcqn)
            det = query.filter(Mcqn.test_id == session['testid']).all()
            return render_to_response('../templates/mcqndisplayquestion.jinja2',{'session' : session,'det' : det},request=request)
        if qtype == "truefalse":
            session['qtype'] = qtype
            query = request.dbsession.query(Truefalse)
            det1 = query.filter(Truefalse.test_id == session['testid']).all()
            return render_to_response('../templates/displayquestion.jinja2',{'session' : session ,'det' : det1},request=request)

        if qtype == "openended":
            session['qtype'] = qtype
            query = request.dbsession.query(DescQuestion)
            det = query.filter(DescQuestion.test_id == session['testid']).all()
        return render_to_response('../templates/displayquestion.jinja2',{'session' : session,'det' : det},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)




@view_config(route_name='optionforadd')
def opt1(request):
    try:
        session = request.session

        qtype = session['qtype']
        if qtype == "mcqn":
            return render_to_response('../templates/mcqnteacherinput.jinja2',{'session' : session},request=request)
        if qtype == "mcq":
            return render_to_response('../templates/mcqteacherinput.jinja2',{'session' : session},request=request)
        if qtype == "truefalse":
            return render_to_response('../templates/tfteacherinput.jinja2',{'session' : session},request=request)
        if qtype == "openended":
            return render_to_response('../templates/desteacherinput.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



##############################################################################################
###TRUE OR FALSE


def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
        print(binaryData)
    return binaryData


@view_config(route_name='tf2')
def tf2(request):
    try:
        session = request.session

        qn = request.params['qname']
        ans = request.params['answer']
        qno = request.params['qno']
        qmark = request.params['qmark']


        query = request.dbsession.query(Truefalse)
        obj = Truefalse()
        obj.Question_name = qn
        obj.Answer = ans
        obj.question_no = qno
        obj.mark = qmark
        obj.test_id = session['testid']
        link=  request.params['qlink']
        obj.qlink = link
        obj.image=request.params['img']

        request.dbsession.add(obj)
        url=request.route_url('ctac')
        return HTTPFound(url)
        return render_to_response('../templates/tfcontinue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

####################################################################################################################
##########TEACHER MCQ STARTS
@view_config(route_name='mcq2')
def mcq2(request):
    try:
        session = request.session


        qmark = request.params['qmark']
        query = request.dbsession.query(Mcq)
        obj = Mcq()

        obj.Question_name = request.params['rqname']
        obj.mark = request.params['qmark']
        obj.question_no = request.params['qno']
        obj.test_id =  session['testid']
        obj.ropt1 = request.params['roption1']
        obj.ropt2 = request.params['roption2']
        obj.ropt3 = request.params['roption3']
        obj.ropt4 = request.params['roption4']
        obj.linkques_name=  request.params['lqname']
        obj.lopt1 = request.params['loption1']
        obj.lopt2 = request.params['loption2']
        obj.lopt3 = request.params['loption3']
        obj.lopt4 = request.params['loption4']
        obj.rcrct = request.params['answer']
        obj.lcrct = request.params['answer1']
        obj.r1l1 = request.params['sug11']
        obj.r1l2 = request.params['sug12']
        obj.r1l3 = request.params['sug13']
        obj.r1l4 = request.params['sug14']
        obj.r2l1 = request.params['sug21']
        obj.r2l2 = request.params['sug22']
        obj.r2l3 = request.params['sug23']
        obj.r2l4 = request.params['sug24']
        obj.r3l1 = request.params['sug31']
        obj.r3l2 = request.params['sug32']
        obj.r3l3 = request.params['sug33']
        obj.r3l4 = request.params['sug34']
        obj.r4l1 = request.params['sug41']
        obj.r4l2 = request.params['sug42']
        obj.r4l3 = request.params['sug43']
        obj.r4l4 = request.params['sug44']
        link=  request.params['qlink']
        obj.qlink = link
        obj.image=request.params['img']
        request.dbsession.add(obj)
        url=request.route_url('ctac')
        return HTTPFound(url)
        return render_to_response('../templates/mcqcontinue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='mcqn2')
def mcqn2(request):
    try:
        session = request.session
        query = request.dbsession.query(Mcqn)
        obj = Mcqn()
        obj.Question_name = request.params['qname']
        obj.mark = request.params['qmark']
        obj.question_no = request.params['qno']
        obj.test_id =  session['testid']
        obj.opt1 = request.params['option1']
        obj.opt2 = request.params['option2']
        obj.opt3 = request.params['option3']
        obj.opt4 = request.params['option4']
        link=  request.params['qlink']
        """filename = request.POST['qnimage'].filename
        input_file = request.POST['qnimage'].file
        file_path = os.path.join('/tmp', '%s.jpg' % uuid.uuid4())
        temp_file_path = file_path
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)"""

    # Now that we know the file has been fully saved to disk move it into place.

        """os.rename(temp_file_path, file_path)
        print(output_file)
        with open(file_path, "rb") as imageFile:
                imagestr = base64.b64encode(imageFile.read())
        print(imagestr)
        print(file_path)"""
        obj.qlink = link
        obj.crct = request.params['answer']
        obj.image=request.params['img']

        request.dbsession.add(obj)
        url=request.route_url('ctac')
        return HTTPFound(url)
        return render_to_response('../templates/mcqcontinue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


########################################################################################################
########Flip Starts


@view_config(route_name='flip')
def flip1(request):
    try:
        session = request.session
        session['cid'] = request.params['courseid']
        query1 = request.dbsession.query(Studentflip)
        z=[]
        query2 = query1.filter(Studentflip.course_id == session['cid']).all()
        for i in query2:
            z.append(i.student_id)
        query1 = request.dbsession.query(Studentcourse)
        det = query1.filter(Studentcourse.course_id == session['cid']).all()
        print(det)
        stud = request.dbsession.query(Student)
        stud_id = []

        count = 0
        for i in det:
            stud_id.append(i.student_id)
            count = count+1
        st_id = []
        name = []
        val=[]
        det1 = [st_id,name,val]
        for i,u in zip(stud_id,stud):
            studdet = stud.filter(i == Student.student_id).all()
            for k in studdet:
                st_id.append(k.student_id)
                name.append(k.name)
                val.append(0)

        for i in range(0,count):
            for j in query2:
                if st_id[i]==j.student_id:
                   val[i]=1


        print(det1)
        print(count)



        return render_to_response('../templates/displayflip.jinja2',{'session' : session,'query' : det1,'count' : count},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(route_name='flipafter')
def flip1after(request):
    try:
        session = request.session

        query = request.dbsession.query(Studentcourse)
        query1 = request.dbsession.query(Studentflip)
        z=[]
        query2 = query1.filter(Studentflip.course_id == session['cid']).all()
        for i in query2:
            z.append(i.student_id)
        det = query.filter(Studentcourse.course_id == session['cid']).all()
        stud = request.dbsession.query(Student)
        stud_id = []

        count = 0
        for i in det:
            stud_id.append(i.student_id)
            count = count+1
        st_id = []
        name = []
        val=[]
        det1 = [st_id,name,val]
        for i,u in zip(stud_id,stud):
            studdet = stud.filter(i == Student.student_id).all()
            for k in studdet:
                st_id.append(k.student_id)
                name.append(k.name)
                val.append(0)

        for i in range(0,count):
            for j in query2:
                if st_id[i]==j.student_id:
                   val[i]=1
        print(det1)
        print(count)
        return render_to_response('../templates/displayflip.jinja2',{'session' : session,'query' : det1,'count' : count},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='flipremove')
def fstore1(request):
    try:
        session = request.session
        session['sid'] = request.params['student_id']
        query = request.dbsession.query(Studentflip)

        query.filter(Studentflip.student_id == session['sid']).delete()
        url=request.route_url('flipafter')
        return HTTPFound(url)
        return render_to_response('../templates/continueflip.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='store')
def store1(request):
    try:
        session = request.session
        session['sid'] = request.params['student_id']
        query = request.dbsession.query(Studentflip)
        obj5 = Studentflip()
        obj5.teacher_id = session['tid']
        obj5.student_id = session['sid']
        obj5.course_id = session['cid']

        request.dbsession.add(obj5)
        url=request.route_url('flipafter')
        return HTTPFound(url)
        return render_to_response('../templates/continueflip.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


#####################################################################################################
##REPORT STARTS
@view_config(route_name='reportcheck')
def reportcheck(request):
    try:
        session = request.session
        tid = session['tid']
        tabledata = request.dbsession.query(Course)
        coursedet = tabledata.filter(Course.teacher_id == tid).all()


        return render_to_response('../templates/reportdisplaycourse.jinja2',{'session' : session, 'course' : coursedet, },request=request)

    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)
@view_config(route_name='category')
def category(request):
  try:
      session = request.session
      return render_to_response('../templates/category.jinja2',{'session' : session},request=request)
  except DBAPIError:
   return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='reportchecktest')
def reportchecktest(request):
  try:
    query1 = request.dbsession.query(Studentcourse)
    query6 = request.dbsession.query(Test)
    session = request.session

    cid = session['cid']
    det1 = query1.filter(Studentcourse.course_id == cid).all()
    #stid = []
    #details = [stid]
    stud_id = []
    stdid = []
    name = []
    count = 0
    details1 = [stud_id,name]
    for i in det1:
        stud_id.append(i.student_id)
        count = count+1

    query2 = request.dbsession.query(Student)

    for i in stud_id:
        det = query2.filter(Student.student_id == i).all()
        for k in det:
            stdid.append(k.student_id)
            name.append(k.name)
    x=[[]]

    for i in query6:
        testdet = query6.filter(Test.courseid == session['cid']).all()
    for j in testdet:
            x.append([])
    details1+x
    print(details1+x)

    print(x)
    print(count)
    print(details1)


    return render_to_response('../templates/teacherreportview.jinja2',{'session' : session,'query' : details1,'count' : count},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='finalreport')
def finalreport(request):
    try:
        session = request.session
        session['sid'] = request.params['student_id']
        query = request.dbsession.query(Studentattendance)
        det = query.filter((Studentattendance.student_id == session['sid']) & (Studentattendance.course_id == session['cid'])).all()
        return render_to_response('../templates/finalreportview.jinja2',{'session' : session,'query' : det},request=request)
    except DBAPIError:
       return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='reportdownload1')
def reportdownload1(request):
 try:
        query1 = request.dbsession.query(Studentcourse)
        query7= request.dbsession.query(Studentattendance)
        query6 = request.dbsession.query(Test)
        session = request.session

        cid = session['cid']
        det1 = query1.filter(Studentcourse.course_id == cid).all()
        #stid = []
        #details = [stid]
        stud_id = []
        stdid = []
        name = []
        test=[]
        mark=[]
        test_name=[]
        count = 0
        """stdid.append('Student ID')
        name.append('Student Name')"""
        details1 = [test,test_name,mark]
        for i in det1:
            stud_id.append(i.student_id)
            count = count+1

        query2 = request.dbsession.query(Student)

        for i in stud_id:
            det = query2.filter(Student.student_id == i).all()
            for k in det:
                stdid.append(k.student_id)
                name.append(k.name)
                mark.append("Absent")
        x=[[]]

        count2=0
        testdet = query6.filter(Test.courseid == session['cid']).all()
        for j in testdet:
                count2+=1
                test.append(j.test_id)
                test_name.append(j.test_name)
        a=0
        for j,i in zip(range(2,count2),range(0,count2)):
            details1[j]=test[i]
        for u in range(0,count):
         a+=1
         for v in query7:
             for w in range(0,count2):
                 student1=query7.filter((Studentattendance.course_id==session['cid'])&(Studentattendance.student_id==stdid[u])&(Studentattendance.test_id==test[w])).all()
                 print(student1)
                 for z in student1:
                     if z.attendance=="present":
                         mark[u]=z.mark

        print(a)
        print(test,test_name,mark)
        test.insert(0,"TEST ID")
        test_name.insert(0,"TEST NAME")
        mark.insert(0,"MARK")

        csv=details1
        rez = [[details1[j][i] for j in range(len(details1))] for i in range(len(details1[0]))]
        csv = rez
        print(csv)
        return excel.make_response_from_array(csv, "xls")

 except DBAPIError:
    return Response(db_err_msg, content_type='text/plain', status=500)





@view_config(route_name='testwise2')
def testwise2(request):
  try:
    query1 = request.dbsession.query(Test)
    session = request.session

    cid = session['cid']
    det = query1.filter(Test.courseid == cid).all()
    id1 = " "
    for i in det:
        id1 = i.test_id

    return render_to_response('../templates/testwise2.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='tviewattendance2')
def tviewattendance2(request):
    try:

        session = request.session
        tid = request.params['test_id']
        session['test_id']=request.params['test_id']
        query1= request.dbsession.query(Studentcourse).filter(Studentcourse.course_id == session['cid']).all()
        stud_id=[]
        stud_name =[]
        attendance=[]
        count=0
        percent=[]
        mark=[]
        for i in query1:
            count+=1
            stud_id.append(i.student_id)
            mark.append('-')
            percent.append(0)
        print(stud_id)
        query2= request.dbsession.query(Student)
        for j,z in zip(range(0,count),query2):
            query3=query2.filter(Student.student_id == stud_id[j]).all()
            for k in query3:
                stud_name.append(k.name)

        print(stud_id,stud_name)
        query4=request.dbsession.query(Studentattendance)

        for i in range(0,count):
            print('1helloooooooooooooooooo')
            query5 = query4.filter((Studentattendance.test_id ==tid) & (Studentattendance.course_id == session['cid']) & (Studentattendance.student_id == stud_id[i])).all()
            for y in query5:
                print('2heloooooooooooooooooo')
                if y.attendance=='present':
                    mark[i]=y.mark

                    percent[i]=y.mark
        print(stud_id,stud_name,mark)
        print(count)

        return render_to_response('../templates/tviewattendance2.jinja2',{'session' : session,'a':percent,'count':count,'stud_id':stud_id,'stud_name':stud_name,'mark':mark},request=request)

    except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='reportdownload2')
def reportdownload2(request):
    try:
        session = request.session
        tid =session['test_id']

        query1= request.dbsession.query(Studentcourse).filter(Studentcourse.course_id == session['cid']).all()
        stud_id=[]
        stud_name =[]
        attendance=[]
        count=0
        percent=[]
        mark=[]
        details1=[stud_id,stud_name,mark]
        for i in query1:
            count+=1
            stud_id.append(i.student_id)
            mark.append('-')
            percent.append(0)
        print(stud_id)
        query2= request.dbsession.query(Student)
        for j,z in zip(range(0,count),query2):
            query3=query2.filter(Student.student_id == stud_id[j]).all()
            for k in query3:
                stud_name.append(k.name)

        print(stud_id,stud_name)
        query4=request.dbsession.query(Studentattendance)

        for i in range(0,count):
            print('1helloooooooooooooooooo')
            query5 = query4.filter((Studentattendance.test_id ==tid) & (Studentattendance.course_id == session['cid']) & (Studentattendance.student_id == stud_id[i])).all()
            for y in query5:
                print('2heloooooooooooooooooo')
                if y.attendance=='present':
                    mark[i]=y.mark

                    percent[i]=y.mark
        print(stud_id,stud_name,mark)
        print(count)
        stud_id.insert(0,"STUDENT ID")
        stud_name.insert(0,"NAME")
        mark.insert(0,"MARK")
        csv=details1
        rez = [[details1[j][i] for j in range(len(details1))] for i in range(len(details1[0]))]
        csv = rez
        print(csv)

        return excel.make_response_from_array(csv, "xls")
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
###################################################################################################################







#@view_config(route_name='createtest', renderer='../templates/createtest.jinja2')
#@view_config(route_name='q1')
#def qnadd(request):
  #try:
    #if request.POST.get('formone'):
    #    qn= request.params['name']
    #####    query = request.dbsession.query(DescQuestion)
    ##    obj1.Question_name = qn
    #

@view_config(route_name='addcourseform', renderer='../templates/addcourseform.jinja2')
def addc(request):
    try:
        session = request.session

        return render_to_response('../templates/addcourseform.jinja2',{'session' : session },request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='a2')
def a2(request):
    try:
        session = request.session
        query = request.dbsession.query(Studentcourse)
        det = query.filter(Studentcourse.student_id == session['sid']).all()
        courseid = " "
        for i in det:
            courseid = i.course_id

        return render_to_response('../templates/studentdisplaycourse.jinja2',{'session' : session,'course' : det},request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)







@view_config(route_name='a1')
def studentcourseadd(request):
    try:
        query = request.dbsession.query(Course)
        session = request.session
        cname = request.params['cname']
        cid = request.params['course_id']
        coursedet = query.filter(Course.course_id == cid).first()
        if coursedet.course_name == cname:
            query2 = request.dbsession.query(Studentcourse)
            obj = Studentcourse()
            obj.student_id = session['sid']
            obj.course_name = cname
            obj.course_id = cid
            request.dbsession.add(obj)
            url=request.route_url('a2')
            return HTTPFound(url)
            return render_to_response('../templates/studentcontinuecourse.jinja2',{'session' : session },request=request)
        else:
            return render_to_response('../templates/addcourseform.jinja2',{'session' : session ,'error' : 'Course doesnt exist' },request=request)

    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='studentchecktest')
def checktest1(request):
  try:
    query1 = request.dbsession.query(Test)
    query3 = request.dbsession.query(Studentattendance)
    session = request.session
    session['cid'] = request.params['course_id']
    cid = session['cid']
    det = query1.filter(Test.courseid == cid).all()
    currentDT = datetime.date.today()
    print(currentDT)
    a=[]
    b=[]
    c = []
    z=[]
    d=[a,b,c,z]
    e=[]
    f=[]

    count=0
    counter=0
    for i in det:
        if i.student_id != session['sid']:

            count+=1
            a.append(i.test_id)
            b.append(i.test_name)
            c.append(0)
        if currentDT < i.end_date:
            z.append(1)
        else:
            z.append(0)
    query5 = query3.filter(Studentattendance.student_id == session['sid']).all()
    print(query5)
    counter=0
    for j in query5:
        counter+=1

        e.append(j.test_id)
        f.append(j.attendance)

    for i in range(0,count):
        for j in range(0,counter):
            if a[i]==e[j] :
                print("if")
                c[i]=1


    print(e,f)
    print(a, b, c,z)
    print(counter)
    """testdet = query3.filter((Studentattendance.student_id == session['sid']) & (Studentattendance.course_id == session['cid'])).all()
    for i in det:"""


    return render_to_response('../templates/studentdisplaytest.jinja2',{'session' : session,'query' : d,'a':a,'b':b,'c':c,'z':z,'count':count},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='taketest')
def taketest(request):
  try:
      session = request.session
      session['testid'] = request.params['test_id']
      query = request.dbsession.query(Test)
      det = query.filter(Test.test_id == session['testid'])
      for i in det:
          session['qtype'] = i.questiontype
      if  session['qtype'] == "mcq":
            question = request.dbsession.query(Mcq)
            questiondet = question.filter(Mcq.test_id == session['testid']).all()
            return render_to_response('../templates/mcqstudenttest.jinja2',{'session' : session,'question' : zip(questiondet,range(len(questiondet)))},request=request)
      if  session['qtype'] == "mcqn":
             question = request.dbsession.query(Mcqn)
             questiondet = question.filter(Mcqn.test_id == session['testid']).all()

             return render_to_response('../templates/mcqnstudenttest.jinja2',{'session' : session,'question' : zip(questiondet,range(len(questiondet)))},request=request)
      if  session['qtype'] == "openended":
          question = request.dbsession.query(DescQuestion)
          questiondet = question.filter(DescQuestion.test_id == session['testid']).all()
          return render_to_response('../templates/desstudenttest.jinja2',{'session' : session,'question' : zip(questiondet,range(len(questiondet)))},request=request)
      if  session['qtype'] == "truefalse":
          question1 = request.dbsession.query(Truefalse)
          questiondet1 = question1.filter(Truefalse.test_id == session['testid']).all()
          return render_to_response('../templates/tfstudenttest.jinja2',{'session' : session,'question' : zip(questiondet1,range(len(questiondet1)))},request=request)
  except DBAPIError:
      return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='validate')
def val(request):
 try:
    session = request.session
    query = request.dbsession.query(DescQuestion)
    questiondet = query.filter(DescQuestion.test_id == session['testid']).all()

    #count = query.filter(DescQuestion.test_id == session['testid']).count()
    tquesid = []
    tqno = []
    tans = []
    tqmark = []
    ttab =[tquesid,tqno,tans,tqmark]
    count = 0
    squesid = []
    sqno = []
    sans = []
    sqmark = []
    stab =[squesid,sqno,sans,sqmark]
    for i in questiondet:
        tquesid.append(i.question_id)
        tqno.append(i.question_no)
        tans.append(i.Answer)
        tqmark.append(i.qmark)
        squesid.append(i.question_id)
        sqno.append(i.question_no)
        count += 1
    print(count)



    for i in range(0,int(count)):

        sans.append(request.params['ans'+str(i)])
        print('first for')


    totalmark = 0
    maxmark = 0
    for i in range(0,int(count)):
            answer_key = ttab[2][i]
            answer = stab[2][i]
            #ans.append(ans)
            #print (answer)
            #ques.append(tablelis[2][i])
            #print (answer_key)
            documents = [answer_key,answer]
            documents = list(map(str, documents))
            print (documents)
            print ("1")
            lemmer = nltk.stem.WordNetLemmatizer()
            print ("2")
            print("second for")
            '''lemmer = nltk.stem.WordNetLemmatizer()
            def LemTokens(tokens):
                return [lemmer.lemmatize(token) for token in tokens]
            remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
            def LemNormalize(text):
                return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))'''




            def LemTokens(tokens):
                print ("3")
                return [lemmer.lemmatize(token) for token in tokens]

            def LemNormalize(text):
                print ("4")
                tokens = nltk.word_tokenize(text)
                words = [w.lower() for w in tokens if w.isalnum()]
                return LemTokens(words)
            print ("5")
            TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
            print ("6")
            def cos_similarity(textlist):
                print(textlist)
                print ("7")
                tfidf = TfidfVec.fit_transform(textlist)
                return (tfidf * tfidf.T).toarray()
            print ("8")
            print(documents)
            tf_matrix = cos_similarity(documents)
            print ("9")
            tfidfTran = TfidfTransformer(norm="l2")
            print ("10")
            tfidfTran.fit(tf_matrix)
            print ("12")
            tfidf_matrix = tfidfTran.transform(tf_matrix)
            cos_similarity_matrix = (tfidf_matrix * tfidf_matrix.T).toarray()
            mk = ttab[3][i]
            score = cos_similarity_matrix[0][1]*mk
            mark = int(round(score))
            print(mark)
            totalmark += mark
            maxmark += ttab[3][i]
            #sqmark.append(mark)
            #print (mark)
            #leng = int(len(mark_list))
            querydet = request.dbsession.query(StudentDescmark)
            obj = StudentDescmark()
            obj.student_id1 = session['sid']
            obj.course_id1 = session['cid']
            obj.test_id1 = session['testid']
            obj.qid1 = ttab[0][i]
            obj.mark = mark
            request.dbsession.add(obj)
    percent = 100*(totalmark/maxmark)
    query5 = request.dbsession.query(Studentattendance)
    obj1 = Studentattendance()
    obj1.student_id = session['sid']
    obj1.course_id = session['cid']
    obj1.test_id = session['testid']
    obj1.mark = totalmark
    obj1.maxmark = maxmark
    obj1.percentage = percent
    obj1.attendance = "present"
    request.dbsession.add(obj1)
    return render_to_response('../templates/welcome.jinja2',{'session' : session},request=request)
 except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(route_name='tfvalidate')
def tfval(request):
 try:
    session = request.session
    query = request.dbsession.query(Truefalse)
    questiondet = query.filter(Truefalse.test_id == session['testid']).all()

    #count = query.filter(DescQuestion.test_id == session['testid']).count()
    tquesid = []
    tqno = []
    tans = []
    tqmark = []
    ttab =[tquesid,tqno,tans,tqmark]
    count = 0
    squesid = []
    sqno = []
    sans = []
    sqmark = []
    stab =[squesid,sqno,sans,sqmark]
    for i in questiondet:
        tquesid.append(i.question_id)
        tqno.append(i.question_no)
        tans.append(i.Answer)
        tqmark.append(i.mark)
        squesid.append(i.question_id)
        sqno.append(i.question_no)
        count += 1
    print(count)



    for i in range(0,int(count)):

        sans.append(request.params['ans'+str(i)])
        print('first for')
    print(stab[2][0])

    totalmark = 0
    maxmark = 0

    mark = 0
    print('hello')
    for i in range(0,int(count)):
            print('second for1')
            answer_key = ttab[2][i]
            answer = stab[2][i]
            if ttab[2][i] == stab[2][i] :
                mark = ttab[3][i]


            else:
                print('elif')
                mark = 0

            totalmark += mark
            print(totalmark)
            maxmark += ttab[3][i]
            print(maxmark)
            #leng = int(len(mark_list))
            querydet = request.dbsession.query(Studenttfmark)
            obj = Studenttfmark()
            obj.student_id = session['sid']
            obj.course_id = session['cid']
            obj.test_id = session['testid']
            obj.qid = ttab[0][i]
            obj.mark = mark
            request.dbsession.add(obj)
    percent = 100*(totalmark/maxmark)
    query5 = request.dbsession.query(Studentattendance)
    obj1 = Studentattendance()
    obj1.student_id = session['sid']
    obj1.course_id = session['cid']
    obj1.test_id = session['testid']
    obj1.mark = totalmark
    obj1.maxmark = maxmark
    obj1.percentage = percent
    obj1.attendance = "present"
    request.dbsession.add(obj1)
    return render_to_response('../templates/welcome.jinja2',{'session' : session},request=request)
 except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

"""@view_config(route_name='mcqperformance', renderer='../templates/mcqperformance.jinja2')
def addcdfxg123(request):
    try:
        session = request.session
        return render_to_response('../templates/mcqperformance.jinja2',{'session' : session },request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)
"""

@view_config(route_name='mcqvalidate')
def mcqvalui(request):
 try:
    session = request.session
    query = request.dbsession.query(Mcq)
    questiondet = query.filter(Mcq.test_id == session['testid']).all()

    #count = query.filter(DescQuestion.test_id == session['testid']).count()
    tquesid = []
    tqno = []
    trans = []
    tlans = []
    tqmark = []
    tropt1 = []
    tropt2 = []
    tropt3 = []
    tropt4 = []
    tlopt1 = []
    tlopt2 = []
    tlopt3 = []
    tlopt4 = []
    r1l1 = []
    r1l2 = []
    r1l3 = []
    r1l4 = []
    r2l1 = []
    r2l2 = []
    r2l3 = []
    r2l4 = []
    r3l1 = []
    r3l2 = []
    r3l3 = []
    r3l4 = []
    r4l1 = []
    r4l2 = []
    r4l3 = []
    r4l4 = []
    ttab =[tquesid,tqno,trans,tlans,tqmark,tropt1,tropt2,tropt3,tropt4,tlopt1,tlopt2,tlopt3,tlopt4,r1l1,r1l2,r1l3,r1l4,r2l1,r2l2,r2l3,r2l4,r3l1,r3l2,r3l3,r3l4,r4l1,r4l2,r4l3,r4l4]
    count = 0
    squesid = []
    sqno = []
    srans = []
    slans = []
    sqmark = []
    stab =[squesid,sqno,srans,slans,sqmark]
    sug = " "
    for i in questiondet:
        tquesid.append(i.question_id)
        tqno.append(i.question_no)
        trans.append(i.rcrct)
        tlans.append(i.lcrct)
        tqmark.append(i.mark)
        tropt1.append(i.ropt1)
        tropt2.append(i.ropt2)
        tropt3.append(i.ropt3)
        tropt4.append(i.ropt4)
        tlopt1.append(i.lopt1)
        tlopt2.append(i.lopt2)
        tlopt3.append(i.lopt3)
        tlopt4.append(i.lopt4)
        r1l1.append(i.r1l1)
        r1l2.append(i.r1l2)
        r1l3.append(i.r1l3)
        r1l4.append(i.r1l4)
        r2l1.append(i.r2l1)
        r2l2.append(i.r2l2)
        r2l3.append(i.r2l3)
        r2l4.append(i.r2l4)
        r3l1.append(i.r3l1)
        r3l2.append(i.r3l2)
        r3l3.append(i.r3l3)
        r3l4.append(i.r3l4)
        r4l1.append(i.r4l1)
        r4l2.append(i.r4l2)
        r4l3.append(i.r4l3)
        r4l4.append(i.r4l4)

        squesid.append(i.question_id)
        sqno.append(i.question_no)
        count += 1
    print(count)



    for i in range(0,int(count)):

        srans.append(request.params['answer'+str(i)])
        slans.append(request.params['answer1'+str(i)])
        print('first for')
    print(stab)

    totalmark = 0
    maxmark = 0

    mark = 0
    print('hello')
    for i in range(0,int(count)):
            if ttab[2][i] == stab[2][i] and ttab[3][i] == stab[3][i]:
                mark = ttab[4][i]
            else:
                mark = 0

            totalmark += mark
            print(totalmark)
            maxmark += ttab[4][i]
            print(maxmark)
            print(stab[2][i],ttab[5][i])
            if stab[2][i] == ttab[5][i]:

                print("345")
                if stab[3][i] == ttab[9][i]:
                 sug = ttab[13][i]
                elif stab[3][i] == ttab[10][i]:
                  sug = ttab[14][i]
                elif stab[3][i] == ttab[11][i]:
                  sug = ttab[15][i]
                elif stab[3][i] == ttab[12][i]:
                  sug = ttab[16][i]
            elif stab[2][i] == ttab[6][i]:
                print("345")
                if stab[3][i] == ttab[9][i]:
                 sug = ttab[17][i]
                elif stab[3][i] == ttab[10][i]:
                  sug = ttab[18][i]
                elif stab[3][i] == ttab[11][i]:
                  sug = ttab[19][i]
                elif stab[3][i] == ttab[12][i]:
                  sug = ttab[20][i]
            elif stab[2][i] == ttab[7][i]:
                print("345")
                if stab[3][i] == ttab[9][i]:
                 sug = ttab[21][i]
                elif stab[3][i] == ttab[10][i]:
                  sug = ttab[22][i]
                elif stab[3][i] == ttab[11][i]:
                  sug = ttab[23][i]
                elif stab[3][i] == ttab[12][i]:
                  sug = ttab[24][i]
            elif stab[2][i] == ttab[8][i]:
                print("345")
                if stab[3][i] == ttab[9][i]:
                 sug = ttab[25][i]
                elif stab[3][i] == ttab[10][i]:
                  sug = ttab[26][i]
                elif stab[3][i] == ttab[11][i]:
                  sug = ttab[27][i]
                elif stab[3][i] == ttab[12][i]:
                  sug = ttab[28][i]
            print(sug)
            #leng = int(len(mark_list))
            querydet = request.dbsession.query(Studentmcqmark)
            obj = Studentmcqmark()
            obj.student_id = session['sid']
            obj.course_id = session['cid']
            obj.test_id = session['testid']
            obj.qid = ttab[0][i]
            obj.mark = mark
            request.dbsession.add(obj)
    percent = 100*(totalmark/maxmark)
    query5 = request.dbsession.query(Studentattendance)
    obj1 = Studentattendance()
    obj1.student_id = session['sid']
    obj1.course_id = session['cid']
    obj1.test_id = session['testid']
    obj1.mark = totalmark
    obj1.maxmark = maxmark
    obj1.percentage = percent
    obj1.attendance = "present"
    request.dbsession.add(obj1)
    #return render_to_response('../templates/mcqperformance.jinja2',{'session' : session },request=request)
    return render_to_response('../templates/mcqperformance.jinja2',{'session':session,'sug':sug,'question':zip(questiondet,range(len(questiondet)))},request=request)
 except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='mcqnvalidate')
def mcqnval(request):
 try:
    session = request.session
    query = request.dbsession.query(Mcqn)
    questiondet = query.filter(Mcqn.test_id == session['testid']).all()

    #count = query.filter(DescQuestion.test_id == session['testid']).count()
    tquesid = []
    tqno = []
    tans = []

    tqmark = []
    topt1 = []
    topt2 = []
    topt3 = []
    topt4 = []

    ttab =[tquesid,tqno,tans,tqmark,topt1,topt2,topt3,topt4]
    count = 0
    squesid = []
    sqno = []
    sans = []

    sqmark = []
    stab =[squesid,sqno,sans,sqmark]
    sug = " "
    for i in questiondet:
        tquesid.append(i.question_id)
        tqno.append(i.question_no)
        tans.append(i.crct)

        tqmark.append(i.mark)
        topt1.append(i.opt1)
        topt2.append(i.opt2)
        topt3.append(i.opt3)
        topt4.append(i.opt4)

        squesid.append(i.question_id)
        sqno.append(i.question_no)
        count += 1
    print(count)



    for i in range(0,int(count)):

        sans.append(request.params['answer'+str(i)])

        print('first for')
    print(stab[2][0])

    totalmark =0
    maxmark =0

    mark =0
    print('hello')
    for i in range(0,int(count)):
            if tans[i] == sans[i] :
                mark = tqmark[i]
            else:
                mark = 0

            totalmark+=mark
            print(totalmark)
            maxmark+=tqmark[i]
            print(maxmark)

            #leng = int(len(mark_list))
            querydet = request.dbsession.query(Studentmcqmark)
            obj = Studentmcqmark()
            obj.student_id = session['sid']
            obj.course_id = session['cid']
            obj.test_id = session['testid']
            obj.qid = ttab[0][i]
            obj.mark = mark
            request.dbsession.add(obj)
    percent = 100*(totalmark/maxmark)
    query5 = request.dbsession.query(Studentattendance)
    obj1 = Studentattendance()
    obj1.student_id = session['sid']
    obj1.course_id = session['cid']
    obj1.test_id = session['testid']
    obj1.mark = totalmark
    obj1.maxmark = maxmark
    obj1.percentage = percent
    obj1.attendance = "present"
    request.dbsession.add(obj1)
    return render_to_response('../templates/welcome.jinja2',{'session' : session},request=request)
 except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


##########################################################################################################
##############################################################################################################
##########################################################################################################
##############################################################################################################
##########################################################################################################
#####################################################################################################################
######STUDENT FLIP
@view_config(route_name='asateacher')
def asateach(request):
    try:
        session = request.session
        query1 = request.dbsession.query(Studentflip)
        query = query1.filter(Studentflip.student_id == session['sid']).all()
        return render_to_response('../templates/studentdisplayflip.jinja2',{'session' : session,'query' : query},request=request)
    except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='flipstore')
def flipstore(request):
    try:
        session = request.session
        session['cid'] = request.params['course_id']
        query1 = request.dbsession.query(Test)
        #request.dbsession.query()
        det = query1.filter(Test.student_id ==  session['sid']).all()


        return render_to_response('../templates/studdisplayfilptest.jinja2',{'session' : session,'query' : det},request=request)

    except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studenttest1')
def studtest1(request):
    try:
        session = request.session

        return render_to_response('../templates/studenttest.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studenttest2')
def studtest2(request):
    try:
        session = request.session
        query = request.dbsession.query(Test)
        query2 = request.dbsession.query(Studentflip)
        obj = Test()
        obj.test_name = request.params['tname']
        obj.courseid = session['cid']
        obj.questiontype = request.params['qntype']
        obj.student_id = session['sid']
        obj.start_date = request.params['sdate']
        obj.end_date = request.params['edate']

        request.dbsession.add(obj)
        '''request.dbsession.query(Test).filter(Test.questiontype==request.params['qntype']).first()
        request.dbsession.query(Studentflip).filter(Studentflip.student_id==session['sid']).update({'test_id':request.params['qntype']})'''
        qtype = request.params['qntype']

        det = query.filter(Test.test_name == request.params['tname']).all()
        session['qtype'] = qtype
        for i in det:
            session['testid'] = i.test_id
        '''obj2 = Studentflip()
        #fid = []
        sid = []
        cid = []
        tid = []
        testid = []
        store = [fid,sid,cid,tid,testid]
        for i in query2:
            fid.append(i.flip_id)
            sid.append(i.student_id)
            cid.append(i.course_id)
            tid.append(i.teacher_id)'''





        #a = request.dbsession.query(Studentflip)
        #b = a.update().where(Studentflip.student_id == session['sid'] and Studentflip.course_id == session['cid']).values(test_id:session['tid'])
        #a1 = request.dbsession.query(Studentflip).filter(Studentflip.student_id == session['sid'] and Studentflip.course_id == session['cid'])
        #a1.test_id = session['testid']
        #request.dbsession.add(a1)
        #transaction.commit
        if qtype == "mcqn":

            return render_to_response('../templates/mcqnstudentinput.jinja2',{'session' : session},request=request)
        if qtype == "mcq":

            return render_to_response('../templates/mcqstudentinput.jinja2',{'session' : session},request=request)
        if qtype == "truefalse":
            return render_to_response('../templates/tfstudentinput.jinja2',{'session' : session},request=request)
        if qtype == "openended":
            return render_to_response('../templates/desstudentinput.jinja2',{'session' : session},request=request)


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studentdes2')
def studentdes2(request):
    try:
        session = request.session

        qn = request.params['qname']
        ans = request.params['qans']
        qno = request.params['qno']
        qmark = request.params['qmark']
        link=  request.params['qlink']
        '''image=request.params['img']
        print(image)'''
        query = request.dbsession.query(DescQuestion)
        obj = DescQuestion()
        obj.Question_name = qn
        obj.Answer = ans
        obj.question_no = qno
        obj.qmark = qmark

        obj.qlink = link
        obj.image=request.params['img']

        obj.test_id = session['testid']
        request.dbsession.add(obj)
        url=request.route_url('studentctac')
        return HTTPFound(url)
        return render_to_response('../templates/studentcontinue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studentctac')
def studenttestcheck(request):
  try:
    query1 = request.dbsession.query(Test)
    session = request.session
    query2 = request.dbsession.query(Studentflip)
    det1 = query1.filter(Studentflip.course_id == session['cid'] and Studentflip.student_id == session['sid']).all()
    id1 = " "
    for i in det1:
        id1 = i.test_id
    for i in det1:
        det = query1.filter(Test.test_id == i.test_id).all()
    return render_to_response('../templates/studdisplayfilptest.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)
  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

#########################################################################################
########Flipped student true or FALSE
@view_config(route_name='studenttf2')
def studenttf2(request):
    try:
        session = request.session

        qn = request.params['qname']
        ans = request.params['answer']
        qno = request.params['qno']
        qmark = request.params['qmark']
        qlink=str(request.params['qlink'])
        query = request.dbsession.query(Truefalse)
        obj = Truefalse()
        obj.Question_name = qn
        obj.Answer = ans
        obj.question_no = qno
        obj.mark = qmark
        link=  request.params['qlink']
        obj.qlink = link
        obj.image=request.params['img']

        obj.test_id = session['testid']
        request.dbsession.add(obj)
        url=request.route_url('studentctac')
        return HTTPFound(url)
        return render_to_response('../templates/studenttfcontinue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

##############################################################################################
##############################################################################################
#####FLIPPED STUDENT MCQ
@view_config(route_name='studentmcq2')
def studentmcq2(request):
    try:
        session = request.session


        qmark = request.params['qmark']
        query = request.dbsession.query(Mcq)
        obj = Mcq()
        obj.Question_name = request.params['rqname']
        obj.mark = request.params['qmark']
        obj.question_no = request.params['qno']
        obj.test_id =  session['testid']
        obj.ropt1 = request.params['roption1']
        obj.ropt2 = request.params['roption2']
        obj.ropt3 = request.params['roption3']
        obj.ropt4 = request.params['roption4']
        obj.linkques_name=  request.params['lqname']
        obj.lopt1 = request.params['loption1']
        obj.lopt2 = request.params['loption2']
        obj.lopt3 = request.params['loption3']
        obj.lopt4 = request.params['loption4']
        obj.rcrct = request.params['answer']
        obj.lcrct = request.params['answer1']
        obj.r1l1 = request.params['sug11']
        obj.r1l2 = request.params['sug12']
        obj.r1l3 = request.params['sug13']
        obj.r1l4 = request.params['sug14']
        obj.r2l1 = request.params['sug21']
        obj.r2l2 = request.params['sug22']
        obj.r2l3 = request.params['sug23']
        obj.r2l4 = request.params['sug24']
        obj.r3l1 = request.params['sug31']
        obj.r3l2 = request.params['sug32']
        obj.r3l3 = request.params['sug33']
        obj.r3l4 = request.params['sug34']
        obj.r4l1 = request.params['sug41']
        obj.r4l2 = request.params['sug42']
        obj.r4l3 = request.params['sug43']
        obj.r4l4 = request.params['sug44']
        link=  request.params['qlink']
        obj.qlink = link
        obj.image=request.params['img']

        request.dbsession.add(obj)
        url=request.route_url('studentctac')
        return HTTPFound(url)
        return render_to_response('../templates/studentmcqcontinue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


##########################################################################################################
##############################################################################################################

@view_config(route_name='studentmcqn2')
def studentmcqn2(request):
    try:
        session = request.session



        query = request.dbsession.query(Mcqn)
        obj = Mcqn()

        obj.Question_name = request.params['qname']
        obj.mark = request.params['qmark']
        obj.question_no = request.params['qno']
        obj.test_id =  session['testid']
        obj.opt1 = request.params['option1']
        obj.opt2 = request.params['option2']
        obj.opt3 = request.params['option3']
        obj.opt4 = request.params['option4']
        link=  request.params['qlink']
        obj.qlink = link
        obj.crct = request.params['answer']
        obj.image=request.params['img']

        request.dbsession.add(obj)
        url=request.route_url('studentctac')
        return HTTPFound(url)
        return render_to_response('../templates/mcqcontinue.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)













##########################################################################################################
##############################################################################################################
##############################################################################################
#############studentreport starts
@view_config(route_name='studentreportcheck')
def a21(request):
    try:
        session = request.session
        query = request.dbsession.query(Studentcourse)
        det = query.filter(Studentcourse.student_id == session['sid']).all()
        courseid = " "
        for i in det:
            courseid = i.course_id

        return render_to_response('../templates/studentreportdiplaycourse.jinja2',{'session' : session,'course' : det},request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studentfinalreport')
def finalreport2(request):
    try:
        session = request.session
        cid = request.params['course_id']
        session['cid'] = cid
        query1 = request.dbsession.query(Studentattendance)
        det1 = query1.filter((Studentattendance.course_id == cid) & (Studentattendance.student_id == session['sid'])).all()
        print(det1)
        return render_to_response('../templates/studentfinalreportview.jinja2',{'session' : session,'query' : det1},request=request)
    except DBAPIError:
       return Response(db_err_msg, content_type='text/plain', status=500)
################################################################################################
##################################
################
#################
#QUIZ STARTS>>>>

@view_config(route_name='quizcoursecheck')
def check(request):
    try:
        session = request.session
        tid = session['tid']
        tabledata = request.dbsession.query(Course)
        coursedet = tabledata.filter(Course.teacher_id == tid).all()

        return render_to_response('../templates/displaycourseforquiz.jinja2',{'session' : session, 'course' : coursedet, },request=request)

    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='checkquiz')
def checktest123(request):
  try:
    query1 = request.dbsession.query(Quiz)
    session = request.session
    session['cid'] = request.params['course_id']
    cid = session['cid']
    det = query1.filter(Quiz.course_id == cid).all()
    id1 = " "
    for i in det:
        id1 = i.quiz_id

    return render_to_response('../templates/displayquiz.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='quiz1')
def quiz11(request):
    try:
        session = request.session
        return render_to_response('../templates/createquiz.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='dispquizques')
def dispquizques(request):
    try:
        session = request.session
        tid = request.params['quiz_id']
        session['qid'] = tid
        query = request.dbsession.query(Quiz)
        det = query.filter(Quiz.quiz_id == tid).all()
        query = request.dbsession.query(Quizquestion)
        det = query.filter(Quizquestion.quiz_id == session['qid']).all()
        return render_to_response('../templates/displayquizquestion.jinja2',{'session' : session,'det' : det},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


















@view_config(route_name='quiz2')
def quiz2(request):
    try:
        session = request.session

        session['a']= request.params['tname']

        session['b'] = request.params['tno']



        return render_to_response('../templates/quiztemplate.jinja2',{'session' : session},request=request)


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='quiztemplate1')
def quiz21(request):
    try:
        session = request.session


        return render_to_response('../templates/quiztemplate.jinja2',{'session' : session},request=request)


    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)











@view_config(route_name='quizstore')

def quizstore(request):
    try:
        session = request.session


        qmark = request.params['qmark']
        query = request.dbsession.query(Quiz)
        obj1 = Quiz()
        obj1.quiz_name = session['a']
        obj1.course_id = session['cid']
        obj1.quiz_no = session['b']
        request.dbsession.add(obj1)
        d = query.filter(Quiz.quiz_name == session['a'] ).all()
        for i in d:
            a=i.quiz_id
        query = request.dbsession.query(Quizquestion)
        obj = Quizquestion()

        obj.question_name = request.params['qname']
        obj.mark = request.params['qmark']
        obj.question_no = request.params['qno']
        obj.quiz_id = a
        obj.opt1 = request.params['A']
        obj.opt2 = request.params['B']
        obj.opt3 = request.params['C']
        obj.opt4 = request.params['D']
        obj.crctopt = request.params['answer']
        obj.qtime =request.params['appt']
        obj.extension_time =request.params['exttime']
        obj.hint =request.params['hint']

        request.dbsession.add(obj)
        url=request.route_url('quizcoursecheck')
        return HTTPFound(url)
        return render_to_response('../templates/welcomequiz.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)




@view_config(route_name='a12')
def a12(request):
    try:
        session = request.session
        query = request.dbsession.query(Studentcourse)
        det = query.filter(Studentcourse.student_id == session['sid']).all()
        courseid = " "
        for i in det:
            courseid = i.course_id

        return render_to_response('../templates/studentdisplaycourse1.jinja2',{'session' : session,'course' : det},request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studentdisplayquiz1')
def checktest11(request):
  try:
    query1 = request.dbsession.query(Quiz)


    session = request.session
    session['cid'] = request.params['course_id']
    cid = session['cid']
    det = query1.filter(Quiz.course_id == cid).all()


    #testdet = query3.filter((Studentattendance.student_id == session['sid']) & (Studentattendance.course_id == session['cid'])).all()


    return render_to_response('../templates/studentdisplayquiz.jinja2',{'session' : session,'query' : det, },request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='takequiz')
def takequiz(request):
  try:
      session = request.session
      session['qid'] = request.params['quiz_id']
      query = request.dbsession.query(Quiz)
      det = query.filter(Quiz.quiz_id == session['qid'])

      question = request.dbsession.query(Quizquestion)
      questiondet = question.filter(Quizquestion.quiz_id == session['qid']).all()
      b=[]
      a=[]
      c=[]
      d=[]
      e=[]
      f=[]
      a1=[]
      hint=[]
      ext=[]
      for i in questiondet:
          a.append(i.question_name)
          b.append(i.opt1)
          c.append(i.opt2)
          d.append(i.opt3)
          e.append(i.opt4)
          f.append(i.crctopt)
          a1.append(i.qtime)
          hint.append(i.hint)
          ext.append(i.extension_time)

          print(f)
      return render_to_response('../templates/example.jinja2',{'session' : session,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f,'a1':a1,'hint': hint,'ext':ext,'question':zip(questiondet,range(len(questiondet)))},request=request)
  except DBAPIError:
      return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='quizvalidate')
def quizvalidate(request):
 try:
    session = request.session
    query = request.dbsession.query(Quizquestion)
    questiondet = query.filter(Quizquestion.quiz_id == session['qid']).all()

    #count = query.filter(DescQuestion.test_id == session['testid']).count()
    tquesid = []
    tqno = []
    trans = []

    tqmark = []
    tropt1 = []
    tropt2 = []
    tropt3 = []
    tropt4 = []

    ttab =[tquesid,tqno,trans,tqmark,tropt1,tropt2,tropt3,tropt4]
    count = 0
    squesid = []
    sqno = []
    srans = []
    slans = []
    sqmark = []
    stab =[squesid,sqno,srans,slans,sqmark]
    sug = " "
    for i in questiondet:
        tquesid.append(i.question_id)
        tqno.append(i.question_no)
        trans.append(i.crctopt)

        tqmark.append(i.mark)
        tropt1.append(i.opt1)
        tropt2.append(i.opt2)
        tropt3.append(i.opt3)
        tropt4.append(i.opt4)


        squesid.append(i.question_id)
        sqno.append(i.question_no)
        count += 1
    print(count)



    for i in range(0,int(count)):

        srans.append(request.params['answer'+str(i)])

        print('first for')
    print(stab[2][0])

    totalmark = 0
    maxmark = 0

    mark = 0
    print('hello')
    for i in range(0,int(count)):
            if ttab[2][i] == stab[2][i] :
                mark = ttab[3][i]
            else:
                mark = 0

            totalmark += mark
            print(totalmark)
            maxmark += ttab[3][i]
            print(maxmark)

    query5 = request.dbsession.query(Studentquiz)
    obj1 = Studentquiz()


    percent = 100*(totalmark/maxmark)

    obj1 = Studentattendance()
    obj1.student_id = session['sid']
    obj1.course_id = session['cid']
    obj1.quiz_id = session['qid']
    obj1.mark = totalmark

    obj1.percentage = percent
    obj1.attendance = "present"
    request.dbsession.add(obj1)
    return render_to_response('../templates/welcomequizanswer.jinja2',{'session' : session ,'sug' : sug ,'question' : zip(questiondet,range(len(questiondet)))},request=request)
 except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

#######################################################################################################
#######################################################################################################
########################################################################################################
#Discussion forum teacher
@view_config(route_name='discussion')
def discussion(request):

        try:
            session = request.session
            tid = session['tid']
            tabledata = request.dbsession.query(Course)
            coursedet = tabledata.filter(Course.teacher_id == tid).all()

            return render_to_response('../templates/discussioncoursedisplay.jinja2',{'session' : session, 'course' : coursedet, },request=request)

        except DBAPIError:
             return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='checkforum')
def checkforum(request):
  try:
    query1 = request.dbsession.query(Forum)
    session = request.session

    
    det = query1.filter(Forum.course_id == session['cid']).all()
    id1 = " "
    for i in det:
        id1 = i.forum_id

    return render_to_response('../templates/displayforum.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='forumcreate')
def forumcreate(request):
  try:
    query1 = request.dbsession.query(Forum)
    session = request.session

    cid = session['cid']
    obj = Forum()
    obj.forum_topic = request.params['topic']
    obj.course_id = cid
    obj.teacher_id = session['tid']

    request.dbsession.add(obj)
    url=request.route_url('checkforum')
    return HTTPFound(url)

    return render_to_response('../templates/welcomecreateforum.jinja2',{'session' : session},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='foumcreate', renderer='../templates/foumcreate.jinja2')
def foumcreate(request):
  try:

    session = request.session
    return render_to_response('../templates/foumcreate.jinja2',{'session' : session},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='finalforum')
def finalforum(request):
  try:
    query1 = request.dbsession.query(Forum)
    query5 = request.dbsession.query(Comments)
    session = request.session
    det = query1.filter(Forum.course_id == session['cid']).all()
    session['forum_id'] = request.params['forum_id']
    query2 = request.dbsession.query(Comments)
    detail = query2.filter(Comments.forum_id == session['forum_id']).all()

    id1 = " "
    count = 0
    detail = query5.filter(Comments.forum_id == session['forum_id']).all()
    count = len(detail)
    print(count)
    name = []
    comment = []
    detail1 = [name,comment]
    for i in detail:


                if i.student_id is None:
                    name.append(i.tname)
                    comment.append(i.comment)
                else:
                    name.append(i.sname)
                    comment.append(i.comment)
    print(detail1)

    id1 = " "
    #for i in det:
        #id1 = i.comment_id

    return render_to_response('../templates/emoji2.jinja2',{'session' : session, 'query' : detail1,'count': count},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='commentstore')
def commentstore(request):
  try:
    query1 = request.dbsession.query(Comments)
    query7 = request.dbsession.query(Teacher)
    session = request.session
    name = query7.filter(Teacher.teacher_id == session['tid']).all()
    for i in name:
        tname = i.username
    obj = Comments()
    obj.teacher_id = session['tid']
    obj.tname = tname
    obj.forum_id = session['forum_id']
    obj.comment = request.params['comment']
    request.dbsession.add(obj)

    #for i in det:
        #id1 = i.comment_id

    count = 0
    detail = query1.filter(Comments.forum_id == session['forum_id']).all()
    count = len(detail)
    print(count)
    name = []
    comment = []
    detail1 = [name,comment]
    for i in detail:

                if i.student_id is None:
                    name.append(i.tname)
                    comment.append(i.comment)
                else:
                    name.append(i.sname)
                    comment.append(i.comment)
    print(detail1)

    id1 = " "

    return render_to_response('../templates/emoji2.jinja2',{'session' : session, 'query' : detail1,'count': count},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

############################################################################################
###########################################################################################
#Discussion forum student

@view_config(route_name='studentdiscussion')
def studentdiscussion(request):

        try:
            session = request.session
            sid = session['sid']
            query = request.dbsession.query(Studentcourse)
            tdet = query.filter(Studentcourse.student_id == session['sid']).all()
            courseid = " "
            for i in tdet:
                courseid = i.course_id

            return render_to_response('../templates/studdisscusscoursedisplay.jinja2',{'session' : session,'course' : tdet},request=request)
        except DBAPIError:
             return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studcheckforum')
def studcheckforum(request):
  try:
    query1 = request.dbsession.query(Forum)
    session = request.session

    session['cid'] = request.params['course_id']
    det = query1.filter(Forum.course_id == session['cid']).all()
    id1 = " "
    for i in det:
        id1 = i.forum_id

    return render_to_response('../templates/studdisplayforum.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)




@view_config(route_name='studfinalforum')
def sfinalforum(request):
  try:
    query1 = request.dbsession.query(Forum)
    session = request.session
    det = query1.filter(Forum.course_id == session['cid']).all()
    session['forum_id'] = request.params['forum_id']
    query2 = request.dbsession.query(Comments)

    #for i in det:
        #id1 = i.comment_id
    count = 0
    detail = query2.filter(Comments.forum_id == session['forum_id']).all()
    count = len(detail)
    print(count)
    name = []
    comment = []
    detail1 = [name,comment]
    for i in detail:

                if i.student_id is None:
                    name.append(i.tname)
                    comment.append(i.comment)
                else:
                    name.append(i.sname)
                    comment.append(i.comment)
    print(detail1)

    id1 = " "


    return render_to_response('../templates/studfinalforum.jinja2',{'session' : session, 'query' : detail1,'count' : count},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studcommentstore')
def studcommentstore(request):
  try:
    session = request.session
    query1 = request.dbsession.query(Comments)
    query3 = request.dbsession.query(Student)
    name = query3.filter(Student.student_id == session['sid'])
    for i in name:
        sname = i.name

    session = request.session
    obj = Comments()
    obj.sname = sname
    obj.student_id = session['sid']
    obj.forum_id = session['forum_id']
    obj.comment = request.params['comment']
    request.dbsession.add(obj)

    #for i in det:
        #id1 = i.comment_id
    count = 0
    detail = query1.filter(Comments.forum_id == session['forum_id']).all()
    count = len(detail)
    print(count)
    name = []
    comment = []
    detail1 = [name,comment]
    for i in detail:

                if i.student_id is None:
                    name.append(i.tname)
                    comment.append(i.comment)
                else:
                    name.append(i.sname)
                    comment.append(i.comment)
    print(detail1)
    return render_to_response('../templates/studfinalforum.jinja2',{'session' : session, 'query' : detail1,'count' : count},request=request)

  except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)


#########################################################################
##Attendance
@view_config(route_name='z1')
def z1(request):
    try:
        session = request.session
        tid = session['tid']
        tabledata = request.dbsession.query(Course)
        coursedet = tabledata.filter(Course.teacher_id == tid).all()
        return render_to_response('../templates/attendancedisplaycourse.jinja2',{'session' : session, 'course' : coursedet},request=request)

    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='displaybuttons')
def attendancecheck(request):
    try:
        session = request.session
        tid = session['tid']
        session['cid'] = request.params['course_id']



        return render_to_response('../templates/displaybuttons.jinja2',{'session' : session},request=request)

    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='studentwise')
def studentwise(request):

        try:
          query1 = request.dbsession.query(Studentcourse)
          query6 = request.dbsession.query(Test)
          session = request.session

          cid = session['cid']
          det1 = query1.filter(Studentcourse.course_id == cid).all()
          #stid = []
          #details = [stid]
          stud_id = []
          stdid = []
          name = []
          count = 0
          details1 = [stud_id,name]
          for i in det1:
              stud_id.append(i.student_id)
              count = count+1

          query2 = request.dbsession.query(Student)

          for i in stud_id:
              det = query2.filter(Student.student_id == i).all()
              for k in det:
                  stdid.append(k.student_id)
                  name.append(k.name)
          x=[[]]

          for i in query6:
              testdet = query6.filter(Test.courseid == session['cid']).all()
          for j in testdet:
                  x.append([])
          details1+x
          print(details1+x)

          print(x)
          print(count)
          print(details1)


          return render_to_response('../templates/studentwisedisplay.jinja2',{'session' : session,'query' : details1,'count' : count},request=request)

        except DBAPIError:
           return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(route_name='viewattendance')
def viewattendance(request):

        try:
          query1 = request.dbsession.query(Studentattendance)
          query6 = request.dbsession.query(Test)
          session = request.session

          cid = session['cid']
          session['sid'] = request.params['student_id']
          det1 = query6.filter(Test.courseid == cid).all()
          test =[]
          attendance=[]
          percent=[]
          count=0
          for i in det1:
              if currentDT>=i.start_date:
                  count+=1
                  test.append(i.test_id)
                  attendance.append('Absent')
                  percent.append(0)
          print(test)
          for i,u in zip(range(0,count),query1):
              a=query1.filter((Studentattendance.test_id == test[i]) & (Studentattendance.student_id == session['sid'])).all()
              for j in a:
               if j.attendance =='present':
                    attendance[i] ='Present'
                    percent[i]=100
          print(attendance,test,count,percent)
          print(percent)
          return render_to_response('../templates/dispfinalattendance.jinja2',{'session' : session,'test' : test,'attendance':attendance,'a':percent,'count' : count},request=request)

        except DBAPIError:
           return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='swreportdownload')
def swreport1(request):
    try:
        query1 = request.dbsession.query(Studentattendance)
        query6 = request.dbsession.query(Test)
        session = request.session
        cid = session['cid']
        det1 = query6.filter(Test.courseid == cid).all()
        test =[]
        attendance=[]
        percent=[]
        count=0
        det=[test,attendance]
        """test.append("Test ID")
        attendance.append("Attendance")"""
        for i in det1:
          if currentDT>=i.start_date:
              count+=1
              test.append(i.test_id)
              attendance.append('Absent')
              percent.append(0)
        print(test)
        for i,u in zip(range(0,count),query1):
          a=query1.filter((Studentattendance.test_id == test[i]) & (Studentattendance.student_id == session['sid'])).all()
          for j in a:
              if j.attendance =='present':
                attendance[i] ='Present'
                percent[i]=100
        print(attendance,test,count,percent)
        print(det)

        """a.append("TEST ID")
        b.append("ATTENDANCE")
        for i in det:"""
        test.insert(0,"TEST ID")
        attendance.insert(0,"ATTENDANCE")

        rez = [[det[u][v] for u in range(len(det))] for v in range(len(det[0]))]
        csv = rez
        print(det)

        return excel.make_response_from_array(csv, "xls")

    except DBAPIError:
       return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='testwise')
def testwise(request):

      try:
        query1 = request.dbsession.query(Test)
        session = request.session

        cid = session['cid']
        det = query1.filter(Test.courseid == cid).all()
        id1 = " "
        for i in det:
            id1 = i.test_id

        return render_to_response('../templates/testwise.jinja2',{'session' : session, 'id' : id1, 'query' : det},request=request)

      except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(route_name='tviewattendance')
def tviewattendance(request):
    try:

        session = request.session
        tid = request.params['test_id']
        session['test_id']=request.params['test_id']
        query1= request.dbsession.query(Studentcourse).filter(Studentcourse.course_id == session['cid']).all()
        stud_id=[]
        stud_name =[]
        attendance=[]
        count=0
        percent=[]
        for i in query1:
            count+=1
            stud_id.append(i.student_id)
            attendance.append('Absent')
            percent.append(0)
        print(stud_id)
        query2= request.dbsession.query(Student)
        for j,z in zip(range(0,count),query2):
            query3=query2.filter(Student.student_id == stud_id[j]).all()
            for k in query3:
                stud_name.append(k.name)

        print(stud_id,stud_name)
        query4=request.dbsession.query(Studentattendance)

        for i in range(0,count):
            print('1helloooooooooooooooooo')
            query5 = query4.filter((Studentattendance.test_id ==tid) & (Studentattendance.course_id == session['cid']) & (Studentattendance.student_id == stud_id[i])).all()
            for y in query5:
                print('2heloooooooooooooooooo')
                if y.attendance=='present':
                    attendance[i]='Present'
                    percent[i]=100
        print(stud_id,stud_name,attendance,percent)
        print(count)

        return render_to_response('../templates/tviewattendance.jinja2',{'session' : session,'a':percent,'count':count,'stud_id':stud_id,'stud_name':stud_name,'attendance':attendance},request=request)

    except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='twreportdownload')
def twreport(request):
    try:
        session = request.session
        tid = session['test_id']
        query1= request.dbsession.query(Studentcourse).filter(Studentcourse.course_id == session['cid']).all()
        stud_id=[]
        stud_name =[]
        attendance=[]
        count=0
        percent=[]
        det=[stud_id,stud_name,attendance]
        stud_id.append("Student ID")
        stud_name.append("Student Name")
        attendance.append("Attendance")
        for i in query1:

            stud_id.append(i.student_id)
            attendance.append('Absent')
            percent.append(0)
            count+=1
        print(stud_id)
        query2= request.dbsession.query(Student)
        for j,z in zip(range(1,count+1),query2):
            query3=query2.filter(Student.student_id == stud_id[j]).all()
            for k in query3:
                stud_name.append(k.name)

        print(stud_id,stud_name)
        query4=request.dbsession.query(Studentattendance)

        for i in range(1,count):
            print('1helloooooooooooooooooo')
            query5 = query4.filter((Studentattendance.test_id ==tid) & (Studentattendance.course_id == session['cid']) & (Studentattendance.student_id == stud_id[i])).all()
            for y in query5:
                print('2heloooooooooooooooooo')
                if y.attendance=='present':
                    attendance[i]='Present'
                    percent[i]=100
        print(stud_id,stud_name,attendance)
        print(count)

        rez = [[det[j][i] for j in range(len(det))] for i in range(len(det[0]))]
        csv = rez
        print(rez)

        return excel.make_response_from_array(csv, "xls")
    except DBAPIError:
     return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='sattendance')
def a22(request):
    try:
        session = request.session
        query = request.dbsession.query(Studentcourse)
        det = query.filter(Studentcourse.student_id == session['sid']).all()
        courseid = " "
        for i in det:
            courseid = i.course_id

        return render_to_response('../templates/sattendancecoursedisp.jinja2',{'session' : session,'course' : det},request=request)
    except DBAPIError:
         return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='sattfinaldisp')
def a23(request):

        try:
          query1 = request.dbsession.query(Studentattendance)
          query6 = request.dbsession.query(Test)
          session = request.session

          session['cid']=request.params['course_id']

          det1 = query6.filter(Test.courseid == session['cid']).all()
          test =[]
          attendance=[]
          count=0
          percent=[]
          for i in det1:
              if currentDT>=i.start_date:
                  count+=1
                  test.append(i.test_id)
                  attendance.append('Absent')
                  percent.append(0)
          print(test)
          for i,u in zip(range(0,count),query1):
              a=query1.filter((Studentattendance.test_id == test[i]) & (Studentattendance.course_id == session['cid']) & (Studentattendance.student_id == session['sid'])).all()\

              for j in a:
                  print('j')
                  if j.attendance =='present':
                    attendance[i] ='Present'
                    percent[i] = 100
          print(attendance,test,count)
          """for q in range(0,len(attendance)):
              if attendance[q]=="Present":
                  percent[q]=100
              else:
                  percent[q]=0"""
          print(percent)
          return render_to_response('../templates/sfinalattendance.jinja2',{'session' : session,'a':percent,'test' : test,'attendance':attendance,'count' : count},request=request)

        except DBAPIError:
           return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='sattfinaldisp2')
def a232(request):

        try:
          query1 = request.dbsession.query(Studentattendance)
          query6 = request.dbsession.query(Test)
          session = request.session


          fdate=request.params['fdate']
          tdate=request.params['tdate']


          det1 = query6.filter((Test.courseid == session['cid'])&(Test.start_date>=fdate) & (Test.start_date<=tdate)).all()

          test =[]
          attendance=[]
          count=0
          percent=[]
          for i in det1:
              if currentDT>=i.start_date:
                  count+=1
                  test.append(i.test_id)
                  attendance.append('Absent')
                  percent.append(0)
          print(test)
          for i,u in zip(range(0,count),query1):
              a=query1.filter((Studentattendance.test_id == test[i]) &(Studentattendance.course_id == session['cid']) & (Studentattendance.student_id == session['sid'])).all()
              for j in a:
                  if j.attendance =='present':
                    attendance[i] ='Present'
                    percent[i] = 100

          print(attendance,test,count)

          """for q in range(0,len(attendance)):
              if attendance[q]=="Present":
                  percent[q]=100
              else:
                  percent[q]=0"""
          print(percent)
          return render_to_response('../templates/sfinalattendance2.jinja2',{'session' : session,'a':percent,'test' : test,'attendance':attendance,'count' : count},request=request)

        except DBAPIError:
           return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='home', renderer='../templates/veryfirst.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'classroom'}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_classroom_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
