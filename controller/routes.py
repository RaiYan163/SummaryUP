from app import app, login_is_required, db
from flask import render_template, redirect, request, flash, url_for, session, abort, make_response,jsonify
from controller import google_auth
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from models import User, Summary, SavedLink, Admin
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from math import ceil


###Log In Part####

def optional_login_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated and 'google_id' not in session:
            flash('You are not logged in. Please log in to access this page.', category='error')
            return redirect(url_for('login'))  # Redirect to the login page
        return view_func(*args, **kwargs)
    return decorated_function





@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect('/dashboard')
            else:
                flash('Incorrect password, try again.', category='error')
            
        
    return render_template("login.html", boolean=True)

@app.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email ID already exists.', category='error')
        elif len(email) < 4:
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
            
             # Create a new User instance
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='pbkdf2:sha256'))

            # Add the new user to the session and commit to the database
            db.session.add(new_user)
            db.session.commit()

            # Log in the new user
            login_user(new_user, remember=True)  # Fixed: use new_user instead of user

            # Notify of successful account creation
            flash('Account Created!', category='success')
    
            # Redirect to the home page or dashboard after successful sign-up
            return redirect('/')
    

    return render_template("signUp.html")


### Login and Logout Stuff
@app.route('/logout')
@optional_login_required
def logout():
    logout_user()
    return redirect("/")




@app.route('/google_login')
def google_login():
    return google_auth.google_login(google_auth.setup_google_auth())



# @app.route('/callback')
# def callback():
#     user_info = google_auth.google_callback(google_auth.setup_google_auth())
#     app.logger.info(f'User info: {user_info}')

#     if user_info:
#         email = user_info['email']
#         name = user_info.get('name', 'Unknown')  # Default name to 'Unknown' if not provided

#         # Check if user already exists
#         user = User.query.filter_by(email=email).first()

#         if user:
#             # User exists, use the existing user
#             login_user(user, remember=True)
#         else:
#             # Create a new User instance
#             new_user = User(email=email, firstName=name, password=generate_password_hash('default_password', method='pbkdf2:sha256'))
#             db.session.add(new_user)
#             db.session.commit()
            
#             # Log in the new user
#             login_user(new_user, remember=True)

#         # Redirect to the dashboard or another page
#         return redirect('/dashboard')
#     else:
#         # Handle login failure
#         app.logger.error('Authentication failed. No user info received.')
#         flash('Authentication failed.', category='error')
#         return redirect(url_for('login'))


@app.route('/callback')
def callback():
    google_auth.google_callback(google_auth.setup_google_auth())
    return redirect("/dashboard")


@app.route('/summary')
@optional_login_required
def summary():
    return render_template('summary.html')


@app.route('/dashboard')
@optional_login_required
def dashboard():
    if current_user.is_authenticated and hasattr(current_user, 'userID') and current_user.userID is not None:
        summaries_count = Summary.query.filter_by(userID=current_user.userID).count()
        links_count = SavedLink.query.filter_by(userID=current_user.userID).count()
    else:
        # Set counts to 0 if userID is nil or user is not authenticated
        summaries_count = 0
        links_count = 0

    return render_template('dashboard.html', 
                           user=current_user, 
                           summaries_count=summaries_count, 
                           links_count=links_count)


@app.route('/show_items')
@optional_login_required
def show_items():
    return render_template('show_items.html')


@app.route('/edit_items')
@optional_login_required
def edit_items():
    return render_template('edit_items.html')


@app.route('/open_items')
@optional_login_required
def open_items():
    return render_template('open_items.html')


@app.route('/save_links')
@optional_login_required
def savelinks():
    return render_template('save_links.html')


@app.route('/settings')
@optional_login_required
def settings():
    return render_template('settings.html')


# @app.route('/showSummary')
# @optional_login_required
# def showSummary():
#     # Define the number of summaries per page
#     per_page = 5
#     page = request.args.get('page', 1, type=int)  # Get the page number from the query parameter

#     # Fetch the total number of summaries for pagination calculation
#     total_summaries = Summary.query.filter_by(userID=current_user.userID).count()

#     # Calculate the total number of pages needed
#     total_pages = ceil(total_summaries / per_page)

#     # Fetch summaries for the current page, sorted by summaryID in descending order
#     summaries = Summary.query.filter_by(userID=current_user.userID)\
#                              .order_by(Summary.summaryID.desc())\
#                              .offset((page - 1) * per_page)\
#                              .limit(per_page)\
#                              .all()

#     return render_template('showSummary.html', summaries=summaries, current_page=page, total_pages=total_pages)

@app.route('/showSummary')
@optional_login_required
def showSummary():
    # Fetch summaries for the user, sorted by summaryID in descending order
    summaries = Summary.query.filter_by(userID=current_user.userID) \
                             .order_by(Summary.summaryID.desc()) \
                             .all()

    return render_template('showSummary.html', summaries=summaries)


# @app.route('/showSummary/<int:summary_id>')
# @optional_login_required
# def showSummary(summary_id):
#     # Fetch the summary with the given summary_id
#     summary = Summary.query.get(summary_id)

#     # Check if the summary exists and belongs to the current user
#     if not summary or summary.userID != current_user.userID:
#         abort(404)  # Return a 404 error if the summary doesn't exist or doesn't belong to the user

#     return render_template('showSummary.html', summary=summary)


@app.route('/showLinks')
@optional_login_required
def showLinks():
    # The category selected by the user from the dropdown menu
    selected_category = request.args.get('category', default=None, type=str)

    # Fetch links based on the selected category for the current logged-in user
    links = []
    if selected_category:
        links = SavedLink.query.filter_by(userID=current_user.userID, linkCategory=selected_category).all()

    return render_template('showLinks.html', links=links, selected_category=selected_category)

@app.route('/linkEdit', methods=['GET', 'POST'])
@optional_login_required
def link_edit():
    if request.method == 'POST':
        link_title = request.form.get('linkTitle')
        link_url = request.form.get('linkURL')
        link_description = request.form.get('description')
        link_category = request.form.get('category')

        # Create a new SavedLink instance
        new_link = SavedLink(
            userID=current_user.userID,
            linkTitle=link_title,
            linkURL=link_url,
            linkDescription=link_description,
            linkCategory=link_category
        )

        # Add the new link to the session and commit to the database
        db.session.add(new_link)
        db.session.commit()

        # Flash a success message
        flash('Link saved successfully!', category='success')
        
        # Redirect to the dashboard
        return redirect(url_for('dashboard'))

    # For GET request, check for the YouTube URL passed as a query parameter
    yt_url = request.args.get('yt_url', '')

    # Render the linkEdit template, passing the YouTube URL if available
    return render_template('linkEdit.html', yt_url=yt_url)

# @app.route('/summaryEdit', methods=['GET', 'POST'])
# @optional_login_required
# def summary_edit():
#     if request.method == 'POST':
#         summary_title = request.form.get('summaryTitle')
#         summary_link = request.form.get('summaryURL')
#         summary_body = request.form.get('body')
#         rating = request.form.get('rating')  # Retrieve the rating from the form

#         # Convert rating to integer, default to None if conversion fails
#         try:
#             rating = int(rating)
#         except ValueError:
#             rating = None

#         # Create a new Summary instance
#         new_summary = Summary(
#             userID=current_user.userID,
#             summaryTitle=summary_title,
#             summaryLink=summary_link,
#             summaryBody=summary_body,
#             rating=rating  # Save the integer rating
#         )

#         # Add the new summary to the session and commit to the database
#         db.session.add(new_summary)
#         db.session.commit()

#         # Flash a success message
#         flash('Summary saved successfully!', category='success')
        
#         # Redirect to a relevant page, such as the dashboard or summary list
#         return redirect(url_for('dashboard'))
    
#     else:
#             # For a GET request, retrieve the query parameters
#             summary_link = request.args.get('summaryURL', '')
#             summary_body = request.args.get('body', '')

#             # Render the template with the pre-filled data
#             return render_template('summaryEdit.html', 
#                                summary_link=summary_link, 
#                                summary_body=summary_body)

@app.route('/summaryEdit', methods=['GET', 'POST'])
@optional_login_required
def summary_edit():
    if request.method == 'POST':
        summary_title = request.form.get('summaryTitle')
        summary_link = request.form.get('summaryURL')
        summary_body = request.form.get('body')
        rating = request.form.get('rating')  # Retrieve the rating from the form

        # Convert rating to integer, default to None if conversion fails
        try:
            rating = int(rating) if rating else None
        except ValueError:
            rating = None

        # Create a new Summary instance
        new_summary = Summary(
            userID=current_user.userID if current_user.is_authenticated else None,
            summaryTitle=summary_title,
            summaryLink=summary_link,
            summaryBody=summary_body,
            rating=rating
        )

        # Add the new summary to the session and commit to the database
        try:
            db.session.add(new_summary)
            db.session.commit()
            flash('Summary saved successfully!', category='success')
        except Exception as e:
            print("Error: ", e)
            flash('An error occurred while saving the summary.', category='error')
        
        return redirect(url_for('dashboard'))
    
    else:
        summary_link = request.args.get('summaryURL', '')
        summary_body = request.args.get('body', '')
        return render_template('summaryEdit.html', summary_link=summary_link, summary_body=summary_body)


   
    









#For Testing Purpose. Delete this later. -Saugata

@app.route('/protected_area')
@optional_login_required
def protected_area():
    return "<a href = '/logout'>Logout</a> <br> <h4> Hello, your email is {} and <br> your name is {}.<\h4>".format(session['email'], session['name']) #This is just a test. You can delete or use this. -Saugata
#The protected area is not done yet. I will do it later. Let me know the info from the gmail. -Saugata


#For the Input and Ouput in the html general.








    
