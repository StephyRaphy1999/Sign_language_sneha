from flask import Flask, render_template, request, redirect,  flash, abort, url_for
from sign import app,mail
from sign.models import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os

from PIL import Image
from flask_session import Session 
from flask import session
from flask_login import login_required
from flask_mail import Message
from datetime import datetime
# from PIL import image

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
        teacher=registration.query.filter_by(email=email,password=password, usertype= 'teacher').first()
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
         
        elif teacher:
            session['uid']=teacher.id
            session['ut']=teacher.usertype

            login_user(teacher)
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

@app.route('/teacher')
def teacher():
    return render_template("teacher.html")

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



@app.route('/logout')
@login_required
def logout():
    print("Before logout code")
    print("----11----")
    try:
        print("----1----")
        logout_user()
        session.clear()  # Clear the session data
        print("Logout successful")
        return redirect('/')  # Redirect to the home page or another page after logout
        print("Before logout code")
    except Exception as e:
        print("------2--------")
        print("Logout failed with error:", str(e))
        return redirect('/')

@login_required
@app.route('/userorg')
def userorg():
    a = registration.query.filter_by(usertype="org").all()
    return render_template("userorg.html",a=a)

@login_required
@app.route('/useremp')
def useremp():
    a = registration.query.filter_by(usertype="emp").all()
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

@app.route('/addtech',methods=['GET', 'POST'])
def addtech():

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
        subject= request.form['sub']
        # image = request.files['image']
        # pic_file = save_to_uploads(image)
        # view = pic_file

        
        a = registration.query.filter_by(email=email).first()
        if a:
            return render_template("emp.html",alert=True)
        else:
            my_data = registration(fname=f_name,lname=l_name,address=address,email=email,dob=dob,gender=gender,sub=subject,contact=phone_no,qualification=qualification,experience=experience,password=password,usertype="teacher")
            db.session.add(my_data) 
            db.session.commit()
            return render_template("log.html",alert=True)
    return render_template("addtech.html")

@login_required
@app.route('/view')
def view():
    a = registration.query.filter_by(usertype="teacher").all()
    return render_template("view.html",a=a)


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



@app.route('/add_ne',methods=['GET', 'POST'])
def add_ne():

    if request.method == 'POST':
        f_name = request.form['fname']
        date = request.form['date']
        description= request.form['description']
        image = request.files['image']
        pic_file = save_to_uploads(image)
        view = pic_file 

        my_data = event(fname=f_name,date=date,description=description,Image=view)
        db.session.add(my_data) 
        db.session.commit()
        return render_template("add_ne.html",alert=True)
    return render_template("add_ne.html")




@app.route('/add_job',methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
       
        dates = request.form['date']
        description = request.form['description']
        designation= request.form['designation']
        salary = request.form['salary']
        

        my_data = addjob(description=description,designation=designation,salary=salary)
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/add_job')
    return render_template("add_job.html")

@app.route('/manage_ne')
def manage_ne():
    a = event.query.all()
    return render_template("manage_ne.html",a=a)
    
@login_required
@app.route('/edit_eve/<int:id>',methods=['GET', 'POST'])
def edit_eve(id):
    c= event.query.get_or_404(id)
    if request.method == 'POST':
        
        c. f_name = request.form['fname']
        c. description= request.form['description']
        c. date= request.form['date']
        c.image = request.files['image']
        
        db.session.commit()
        return redirect('/add_ne')
    return render_template("edit_eve.html",c=c)

@login_required
@app.route('/delete_eve/<int:id>')
def delete_eve(id):
    delete= event.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return render_template("index.html",alert2=True)  
    except:
        return 'There was a problem deleting that task'

# add and view job opprunity



        
@login_required
@app.route('/edit_job/<int:id>',methods=['GET', 'POST'])
def edit_job(id):
    c= addjob.query.get_or_404(id)
    if request.method == 'POST':                                
        c.date = request.form['date']
        c.description = request.form['description']
        c.designation= request.form['designation']
        c.salary = request.form['salary']
        
       
        db.session.commit()
        return redirect('/manage_job')
    return render_template("edit_job.html",c=c)

@login_required
@app.route('/delete_job/<int:id>')
def delete_job(id):
    delete= addjob.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()

        return render_template("index.html",alert2=True)
    except:
        return 'There was a problem deleting that task'

@app.route('/manage_job')
def manage_job():
    c= addjob.query.all()
    return render_template("manage_job.html",c=c)


@login_required
@app.route('/apply_jobs/<int:id>', methods=['GET', 'POST'])
def apply_jobs(id):
    job = addjob.query.get_or_404(id)
    print("-----------jobid----------")
    print(job)
    job_id = id
    print(job_id)
    
    user_id = session['uid']
    print("user_id")
    print(user_id)
    c= addjob.query.all()

    if request.method == 'POST':
        image = request.files['resume']
        pic_file = save_to_uploads(image)
        view = pic_file 
        date = datetime.now()

        my_data = apply_job(user_id=user_id, job_id=job_id, resume=view, date=date)
        db.session.add(my_data)
        db.session.commit()
        return render_template("dis_view_job.html",alert=True,c=c)
    
    return render_template("apply_job.html")



@app.route('/dis_view_job')
def dis_view_job():
    c= addjob.query.all()
    print("helloooooo")
    exit()
    return render_template("dis_view_job.html",c=c)

# edit the job and delete

@login_required
@app.route('/edit_tech/<int:id>',methods=['GET', 'POST'])
def edit_tech(id):
    c= registration.query.get_or_404(id)
    if request.method == 'POST':
        
        c. fname = request.form['fname']
        c. lname = request.form['lname']
        c. gender = request.form['gender']
        c. dob = request.form['dob']
        c. address = request.form['address']
        c. email = request.form['email']
        c. phone_no = request.form['contact']
        c. password = request.form['password']
        c. qualification = request.form['qualification']
        c. experience= request.form['experience'] 
        c. subject= request.form['sub']
        # c.image = request.files['image']
        
        db.session.commit()
        return redirect('/addtech')
    return render_template("edit_tech.html",c=c)

@app.route('/viewjob_dis')
def vw_job():
    c= addjob.query.all()
    return render_template("dis_view_job.html",c=c)


@app.route('/apply_manage')
def apply_manage():
    c= apply_job.query.all()
    return render_template("apply_manage.html",c=c)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    delete= registration.query.get_or_404(id)
    try:
        db.session.delete(delete)
        db.session.commit()
        return render_template("index.html",alert2=True)  
    except:
        return 'There was a problem deleting that task'

from PIL import Image
from random import randint
import os

def save_to_uploads(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    print(app.root_path)
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



@login_required
@app.route('/chat_tec',methods=['GET','POST'])
def chat_tech():
    u=current_user.id
    b = registration.query.filter_by(usertype="teacher").all()
    print(b)
    # a = registration.query.filter_by(user_id=u).first()
    if request.method == 'POST':

        message = request.form['message']
        print(message)
        teachers = request.form['teachers']
        print(teachers)

        my_data = chat_tec(user_id=u,message=message,teacher_id=teachers)
        print(my_data)
        db.session.add(my_data)
        print("---------------1---------")
        db.session.commit()
        print("------------2-------------")
        return redirect('/')

    return render_template("chat_tec.html",b=b)

@login_required
@app.route('/view_chat')
def viewchat():
    a = registration.query.filter_by(id=session['uid']).first()
    print(session['uid'])
    b=None
    if a:
        name=a.fname
        print(name)
        b=chat_tec.query.filter_by(teacher_id=name,status="NULL").all()
        print(b)
    return render_template("view_chat.html",a=a,b=b)

@login_required
@app.route('/response/<int:id>',methods=['GET', 'POST'])
def response(id):
    c= chat_tec.query.filter_by(id=id).first()
    print(c.id)
    if request.method == 'POST':
        c.response = request.form['response']
        print(c.response)
        print("___________rrr_________")
        c.status="added"
        print(c.status)
        db.session.commit()
        return redirect('/')
    return render_template("response.html")

@login_required
@app.route('/view_response')
def viewresponse():
    u_id=current_user.id
    print(u_id)
    a = chat_tec.query.filter_by(user_id=u_id).all()
    return render_template("view_response.html",a=a)
