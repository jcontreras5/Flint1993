from flask import Blueprint, render_template, flash, redirect, url_for, request
from Flint1993.forms import UserLoginForm
from Flint1993.models import User, check_password_hash,db #7 include db 
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/register', methods = ['GET','POST']) #1 auth register rte decor fun
def register():
    form = UserLoginForm() #ins of ULF class as form
    # return render_template('signup.html', form = form)  #2 connected signup forms to html by form var
    try:
        if request.method == 'POST' and form.validate_on_submit(): # 2 request goes to template and grabs info from form
            username = form.username.data
            email = form.email.data # 2 user input email
            password = form.password.data #2 user input email
            
            user = User(username, email, password)#3
            db.session.add(user)#3
            db.session.commit()#3 one commit push to db

            #if no errors,then flash,(requires html call) via {msg}
            flash(f'You have successfully created account {email}','user-created')
            #redirect 
            return redirect(url_for('site.home'))
    
    except:
        raise Exception('Invalid form data: please check form')

    return render_template('register.html', form = form) #return register rte here


# sign in
@auth.route('/login', methods = ['GET','POST'])
def login():
    form = UserLoginForm() # ins of ULF class as form
     # same as above 
    try:
        print(form.validate_on_submit())
        if request.method =='POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print('gots data')
            #create var for logged_user
            logged_user = User.query.filter(User.email == email).first() #query table filter == WHERE user.email - email above
            print(logged_user)
            if logged_user and check_password_hash(logged_user.password, password):# if vars exist and not none: 1st arg table pass comparison from table pw to input pw
                print("no")
                login_user(logged_user) #3 logs user in 
                flash('You were successfully logged in: Via Email/Password', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                print("yes")
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form Data: Please check your form')
    print("too")
    return render_template('login.html', form = form) 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))



