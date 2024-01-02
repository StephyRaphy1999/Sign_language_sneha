from sign import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from sqlalchemy import ForeignKey

@login_manager.user_loader
def load_user(id):
    return registration.query.get(int(id))

class registration(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    address= db.Column(db.String (80))
    email= db.Column(db.String(80))
    contact= db.Column(db.String (10))
    password = db.Column(db.String(80))
    usertype = db.Column(db.String(80))
    age = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    dob = db.Column(db.String(80)) 
    Image=db.Column(db.String(80))
    qualification=db.Column(db.String(80))
    experience=db.Column(db.String(80))
    status=db.Column(db.String(80),default='NULL')
    sub=db.Column(db.String(80))

class event(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    Image=db.Column(db.String(80))
    date=db.Column(db.String(80))
    description=db.Column(db.String(80))

class addjob(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    userid= db.Column(db.Integer,ForeignKey('registration.id'))
    date=db.Column(db.String(80))
    description=db.Column(db.String(80))
    designation=db.Column(db.String(80))
    salary=db.Column(db.String(80))

class apply_job(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80))
    description=db.Column(db.String(80))
    image=db.Column(db.String(80))
    date=db.Column(db.String(80))
    

