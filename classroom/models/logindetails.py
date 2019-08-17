
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Date,
    Unicode,
    LargeBinary
)
import sqlalchemy_utils
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from .meta import Base
from sklearn.feature_extraction.text import TfidfTransformer
import nltk,string, numpy
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
from datetime import time
from sqlalchemy_utils import UUIDType
from furl import furl
import uuid
#
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from struct import *
"""
_DeclarativeBase = declarative_base()

class MyTable(_DeclarativeBase):
    __tablename__ = 'mytable'
    id = Column(Integer, Sequence('my_table_id_seq'), primary_key=True)
    my_blob = Column(BLOB)
"""
class Student(Base):
    __tablename__ = 'student'
    student_id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text)
    email_id = Column(Text)
    cid =Column(Integer, ForeignKey('course.course_id'))
    institute_name = Column(Text)
    courses = relationship("Studentcourse",cascade="all, delete-orphan")
    mark = relationship("StudentDescmark",cascade="all, delete-orphan")
    studentflip = relationship("Studentflip",cascade="all, delete-orphan")
    tf = relationship("Studenttfmark",cascade="all, delete-orphan")
    mcq = relationship("Studentmcqmark",cascade="all, delete-orphan")
    quiz = relationship("Studentquiz",cascade="all, delete-orphan")
    test12 = relationship("Test")
class Teacher(Base):
    __tablename__ = 'teacher'
    teacher_id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    email_id = Column(Text)
    subject = Column(Text)
    institute_name = Column(Text)
    courses = relationship("Course")
    studentflip = relationship("Studentflip",cascade="all, delete-orphan")



class Course(Base):
    __tablename__ = 'course'
    course_id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    students = relationship("Student",cascade="all, delete-orphan")
    course_name = Column(Text)
    course_discipline = Column(Text)
    tests = relationship("Test",cascade="all, delete-orphan")
    studentflip = relationship("Studentflip",cascade="all, delete-orphan")
    Quiz = relationship("Quiz",cascade="all, delete-orphan")
    studentquiz = relationship("Studentquiz")
    forum1= relationship("Forum",cascade="all, delete-orphan")
    att1 = relationship("Studentattendance",cascade="all, delete-orphan")
class Test(Base):
    __tablename__ = 'test'
    test_id = Column(Integer, primary_key=True)
    courseid = Column(Integer, ForeignKey('course.course_id'))
    test_name = Column(Text)
    questiontype = Column(Text)
    student_id = Column(Integer, ForeignKey('student.student_id'))
    start_date = Column(Date)
    end_date = Column(Date)
    questions = relationship("DescQuestion",cascade="all, delete-orphan")
    test_no = Column(Integer)
    studentflip = relationship("Studentflip",cascade="all, delete-orphan")
    mcqques = relationship("Mcq",cascade="all, delete-orphan")
    tfquestion = relationship("Truefalse",cascade="all, delete-orphan")
    mcqn =  relationship("Mcqn",cascade="all, delete-orphan")
    att = relationship("Studentattendance",cascade="all, delete-orphan")

class DescQuestion(Base):
    __tablename__ = 'question'
    question_id = Column(Integer, primary_key=True)
    question_no = Column(Integer)
    Question_name = Column(Text)
    test_id =  Column(Integer, ForeignKey('test.test_id'))
    Answer = Column(Text)
    qmark = Column(Integer)
    image = Column(Text)
    qlink = Column(Text)

class Mcq(Base):
    __tablename__ = 'mcq'
    question_id = Column(Integer, primary_key=True)
    Question_name = Column(Text)
    question_no = Column(Integer)
    test_id =  Column(Integer, ForeignKey('test.test_id'))
    mark = Column(Integer)
    ropt1 = Column(Text)
    ropt2 = Column(Text)
    ropt3 = Column(Text)
    ropt4 = Column(Text)
    linkques_name=  Column(Text)
    lopt1 = Column(Text)
    lopt2 = Column(Text)
    lopt3 = Column(Text)
    lopt4 = Column(Text)
    rcrct = Column(Text)
    lcrct = Column(Text)
    r1l1 = Column(Text)
    r1l2 = Column(Text)
    r1l3 = Column(Text)
    r1l4 = Column(Text)
    r2l1 = Column(Text)
    r2l2 = Column(Text)
    r2l3 = Column(Text)
    r2l4 = Column(Text)
    r3l1 = Column(Text)
    r3l2 = Column(Text)
    r3l3 = Column(Text)
    r3l4 = Column(Text)
    r4l1 = Column(Text)
    r4l2 = Column(Text)
    r4l3 = Column(Text)
    r4l4 = Column(Text)
    qlink = Column(Text)
    image = Column(Text)
class Mcqn(Base):
    __tablename__ = 'mcqn'
    question_id = Column(Integer, primary_key=True)
    Question_name = Column(Text)
    question_no = Column(Integer)
    test_id =  Column(Integer, ForeignKey('test.test_id'))
    mark = Column(Integer)
    opt1 = Column(Text)
    opt2 = Column(Text)
    opt3 = Column(Text)
    opt4 = Column(Text)
    crct = Column(Text)
    qlink = Column(Text)
    image = Column(Text)

class Truefalse(Base):
    __tablename__ = 'truefalse'
    question_id = Column(Integer, primary_key=True)
    question_no = Column(Integer)
    Question_name = Column(Text)
    test_id =  Column(Integer, ForeignKey('test.test_id'))
    Answer = Column(Text)
    mark = Column(Integer)
    qlink = Column(Text)
    image = Column(Text)


class Studentcourse(Base):
    __tablename__ = 'studentcourse'
    cs_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))
    course_id =  Column(Integer)
    course_name =  Column(Text)


class StudentDescmark(Base):
    __tablename__ = 'studentdescmark'
    descmarkid = Column(Integer, primary_key=True)
    student_id1 = Column(Integer, ForeignKey('student.student_id'))
    course_id1 =  Column(Integer)
    test_id1 =  Column(Integer)
    qid1 =  Column(Integer)
    mark = Column(Integer)

class Studenttfmark(Base):
    __tablename__ = 'studenttfmark'
    tfmarkid = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))
    course_id =  Column(Integer)
    test_id =  Column(Integer)
    qid =  Column(Integer)
    mark = Column(Integer)

class Studentmcqmark(Base):
    __tablename__ = 'studentmcqfmark'
    mcqmarkid = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))
    course_id =  Column(Integer)
    test_id =  Column(Integer)
    qid =  Column(Integer)
    mark = Column(Integer)


class Studentflip(Base):
    __tablename__ = 'studentflip'
    flip_id = Column(Integer,primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))
    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    course_id  = Column(Integer, ForeignKey('course.course_id'))
    test_id = Column(Integer, ForeignKey('test.test_id'))


class Studentattendance(Base):
    __tablename__ = 'studentattendance'
    mark_id = Column(Integer,primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))
    course_id  = Column(Integer, ForeignKey('course.course_id'))
    test_id = Column(Integer, ForeignKey('test.test_id'))
    mark =  Column(Integer)
    maxmark = Column(Integer)
    percentage = Column(Integer)
    attendance =  Column(Text)

class Quiz(Base):
    __tablename__ = 'quiz'
    quiz_id = Column(Integer,primary_key=True)
    course_id =  Column(Integer, ForeignKey('course.course_id'))
    quiz_no =  Column(Integer)
    quiz_name = Column(Text)
    
    quiz1 =relationship("Quizquestion",cascade="all, delete-orphan")

class Quizquestion(Base):
    __tablename__ = 'quizquestion'
    quizquestion_id = Column(Integer,primary_key=True)
    quiz_id =  Column(Integer, ForeignKey('quiz.quiz_id'))
    question_no = Column(Integer)
    question_name = Column(Text)
    opt1 = Column(Text)
    opt2 = Column(Text)
    opt3 = Column(Text)
    opt4 = Column(Text)
    crctopt = Column(Text)
    best_nextans = Column(Text)
    qtime = Column(Integer)
    extension_time = Column(Integer)
    hint = Column(Text)

class Studentquiz(Base):
    __tablename__ = 'studentquiz'
    stquizid = Column(Integer,primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id'))
    course_id =Column(Integer, ForeignKey('course.course_id'))
    lives = Column(Integer)


class Forum(Base):
    __tablename__ = 'forum'
    student_id = Column(Integer, ForeignKey('student.student_id'))
    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    course_id = Column(Integer, ForeignKey('course.course_id'))
    forum_id =  Column(Integer,primary_key=True)
    forum_topic = Column(Text)
    start_date = Column(Integer)
    end_date = Column(Integer)
    forum = relationship("Comments",cascade="all, delete-orphan")



class Comments(Base):
    __tablename__ = 'comments'
    student_id = Column(Integer, ForeignKey('student.student_id'))
    sname =  Column(Text)
    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    tname = Column(Text)
    comment_id =  Column(Integer,primary_key=True)
    forum_id = Column(Integer, ForeignKey('forum.forum_id'))
    comment =  Column(Text)
    time = Column(Integer)


#Index('my_index', MyModel.name, unique=True, mysql_length=255)
