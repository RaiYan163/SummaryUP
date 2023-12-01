from app import app, login_is_required, db
from flask import render_template, redirect, request, flash, url_for
from controller import google_auth
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from models import User, Summary, SavedLink, Admin
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


###Log In Part####





@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        print(data)
    return render_template("login.html", boolean=True)

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category="error")
            email = request.form.get('email')
        elif len(firstName) < 2:
            flash('FirstName must be greater than 1 characters.', category="error")
            email = request.form.get('email')
            firstName = request.form.get('firstName')
        elif password1 != password2:
            flash('Passwords Dont match', category="error")
            email = request.form.get('email')
            firstName = request.form.get('firstName')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category = 'error')
            email = request.form.get('email')
            firstName = request.form.get('firstName')
        else:
            
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))

            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!',  category = 'success')
            return redirect('/')
    

    return render_template("signUp.html")


### Login and Logout Stuff
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


#For Google Login. -Saugata
@app.route('/google_login')
def google_login():
    return google_auth.google_login(google_auth.setup_google_auth())



@app.route('/callback')
def callback():
    google_auth.google_callback(google_auth.setup_google_auth())
    return redirect("/dashboard")

#For Google Login. -Saugata




@app.route('/summary')
@login_is_required
def summary():
    return render_template('summary.html')


@app.route('/dashboard')
@login_is_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/show_items')
@login_is_required
def show_items():
    return render_template('show_items.html')


@app.route('/edit_items')
@login_is_required
def edit_items():
    return render_template('edit_items.html')


@app.route('/open_items')
@login_is_required
def open_items():
    return render_template('open_items.html')


@app.route('/save_links')
@login_is_required
def savelinks():
    return render_template('save_links.html')


@app.route('/settings')
@login_is_required
def settings():
    return render_template('settings.html')






#For Testing Purpose. Delete this later. -Saugata

@app.route('/protected_area')
@login_is_required
def protected_area():
    return "<a href = '/logout'>Logout</a> <br> <h4> Hello, your email is {} and <br> your name is {}.<\h4>".format(session['email'], session['name']) #This is just a test. You can delete or use this. -Saugata
#The protected area is not done yet. I will do it later. Let me know the info from the gmail. -Saugata