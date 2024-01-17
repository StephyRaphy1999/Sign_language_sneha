from sign import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

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



class addjob(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, ForeignKey('registration.id'))
    uid=relationship('registration',foreign_keys=[user_id])
    date=db.Column(db.String(80))
    description=db.Column(db.String(80))
    designation=db.Column(db.String(80))
    salary=db.Column(db.String(80))

class event(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80))
    Image=db.Column(db.String(80))
    date=db.Column(db.String(80))
    description=db.Column(db.String(80))



class apply_job(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('registration.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('addjob.id'))
    jid = db.relationship('addjob', foreign_keys=[job_id])
    resume = db.Column(db.String(80))
    date = db.Column(db.String(80))
    user = db.relationship('registration', foreign_keys=[user_id])


    
class chat_tec(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, ForeignKey('registration.id'))
    uid=relationship('registration',foreign_keys=[user_id])
    teacher_id= db.Column(db.Integer, ForeignKey('registration.id'))
    tid=relationship('registration',foreign_keys=[teacher_id])
    message=db.Column(db.String(80))
    response=db.Column(db.String(80))