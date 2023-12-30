from flask import Flask, render_template, request, redirect,  flash, abort, url_for
from sign import app,mail
from sign.models import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from flask_session import Session 
from flask import session
from flask_login import login_required
from flask_mail import Message

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/log',methods=['GET', 'POST'])
def log():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        admin = registration.query.filter_by(email=email, password=password,usertype= 'admin').first()
        org=registration.query.filter_by(email=email,password=password, usertype= 'org').first()
        emp=registration.query.filter_by(email=email,password=password, usertype= 'emp').first()
        disabled=registration.query.filter_by(email=email,password=password, usertype= 'disabled').first()
        if admin:
            session['uid']=admin.id
            session['ut']=admin.usertype
            
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/') 
             
        elif org:
            session["uid"]=org.id
            session["ut"]=org.usertype
           
            login_user(org)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/') 
        
        elif emp:
            session['uid']=emp.id
            session['ut']=emp.usertype
            
            login_user(emp)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/') 

        elif disabled:
            session['uid']=disabled.id
            session['ut']=disabled.usertype

            login_user(disabled)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')  
         
        else:
            return render_template("log.html")
    return render_template("log.html")

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/reg')
def register():
    return render_template("reg.html")

# @app.route('/org')
# def org():

#     return render_template("org.html")

@app.route('/emp',methods=['GET', 'POST'])
def emp():
    
    if request.method == 'POST':
        f_name = request.form['fname']
        l_name = request.form['lname']
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address']
        email = request.form['email']
        phone_no = request.form['contact']
        password = request.form['password']
        qualification = request.form['qualification']
        experience= request.form['experience']
        
        a = registration.query.filter_by(email=email).first()
        if a:
            return render_template("emp.html",alert=True)
        else:
            my_data = registration(fname=f_name,lname=l_name,address=address,email=email,dob=dob,gender=gender,contact=phone_no,qualification=qualification,experience=experience,password=password,usertype="emp")
            db.session.add(my_data) 
            db.session.commit()
            return render_template("log.html",alert=True)
    return render_template("emp.html")

@app.route('/disabled',methods=['GET', 'POST'])
def disabled():
    
    if request.method == 'POST':
        f_name = request.form['fname']
        l_name = request.form['lname']
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address']
        email = request.form['email']
        phone_no = request.form['contact']
        password = request.form['password']
        
        a = registration.query.filter_by(email=email).first()
        if a:
            return render_template("emp.html",alert=True)
        else:
            my_data = registration(fname=f_name,lname=l_name,address=address,email=email,dob=dob,gender=gender,contact=phone_no,password=password,usertype="disabled")
            db.session.add(my_data) 
            db.session.commit()
            return render_template("log.html",alert=True)

        return render_template("disabled.html")

@app.route('/org',methods=['GET', 'POST'])
def org():
    if request.method == 'POST':
        org_name = request.form['fname']
        address = request.form['address']
        email = request.form['email']
        phone_no = request.form['contact']
        password = request.form['password']
        
        a = registration.query.filter_by(email=email).first()
        if a:
            return render_template("org.html",alert=True)
        else:
            my_data = registration(fname=org_name,address=address,email=email,contact=phone_no,password=password,usertype="org")
            db.session.add(my_data) 
            db.session.commit()
            return render_template("log.html",alert=True)
    return render_template("org.html")



from flask import Flask, render_template, redirect, session
from flask_login import logout_user, login_required, current_user
from sign import app  # Assuming 'sign' is your Flask application instance







@app.route('/user')
def user():
    return render_template("user.html")

# @app.route('/userorg')
# def userorg():
#     return render_template("userorg.html")

# @app.route('/useremp')
# def useremp():
#     return render_template("useremp.html")

# @app.route('/userdisabled')
# def userdisabled():
#     return render_template("userdisabled.html")

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        session.clear()  # Clear the session data
        print("Logout successful")
        return redirect('/')  # Redirect to the home page or another page after logout
    except Exception as e:
        print("Logout failed with error:", str(e))
        return redirect('/')

@login_required
@app.route('/userorg')
def userorg():
    a = registration.query.filter_by(usertype="org",status="NULL").all()
    return render_template("userorg.html",a=a)

@login_required
@app.route('/useremp')
def useremp():
    a = registration.query.filter_by(usertype="emp",status="NULL").all()
    return render_template("useremp.html",a=a)

@login_required
@app.route('/userdisabled')
def userdisabled():
    a = registration.query.filter_by(usertype="disabled").all()
    return render_template("userdisabled.html",a=a)

@login_required
@app.route('/approve_org/<int:id>')
def approve_org(id):
    c= registration.query.get_or_404(id)
    c.status = 'approve'
    db.session.commit()
    a_sendmail(c.email)
    return redirect('/userorg')

@app.route('/reject_org/<int:id>')
@login_required
def reject_org(id):
    c= registration.query.get_or_404(id)
    c.status = 'reject'
    db.session.commit()
    r_sendmail(c.email)
    return redirect('/userorg')

@login_required
@app.route('/approve_emp/<int:id>')
def approve_emp(id):
    c= registration.query.get_or_404(id)
    c.status = 'approve'
    db.session.commit()
    a_sendmail(c.email)
    return redirect('/useremp')

@app.route('/reject_emp/<int:id>')
@login_required
def reject_emp(id):
    c= registration.query.get_or_404(id)
    c.status = 'reject'
    db.session.commit()
    r_sendmail(c.email)
    return redirect('/useremp')

def r_sendmail(email):
    msg = Message('Registeration Rejected',
                  recipients=[email])
    msg.body = f''' Sorry , Your  Registeration is rejected. '''
    mail.send(msg)




def a_sendmail(email):
    msg = Message('Approved Successfully',recipients=[email])
    msg.body = f''' Congratulations , Your  Registeration is approved successfully... Now You can login using email id and password '''
    mail.send(msg)



#  @app.route('/reject_contributor/<int:id>')
# @login_required
# def reject_contributor(id):
#     c= Register.query.get_or_404(id)
#     c.status = 'reject'
#     db.session.commit()
#     r_sendmail(c.email)
#     return redirect('/vw_contributors')

# def r_sendmail(email):
#     msg = Message('Registeration Rejected',
#                   recipients=[email])
#     msg.body = f''' Sorry , Your  Registeration is rejected. '''
#     mail.send(msg)
