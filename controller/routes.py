from app import app, login_is_required, db
from flask import render_template, redirect, url_for, flash
from controller import google_auth
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from models import User, Summary, SavedLink, Admin
from forms import LoginForm


###Log In Part####

login = LoginManager(app)  

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/login', methods=['POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.userEmail.data).first()

        # Ensure that the user is not None and the password field is not None
        if user and user.password is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            # If login doesn't succeed, send an error message back to the form
            flash('Invalid username or password')

    return render_template('index.html', form=form)







@app.route('/', methods=['GET'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

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