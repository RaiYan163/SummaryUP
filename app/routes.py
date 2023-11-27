# routes.py
from flask import Blueprint, render_template, session, redirect, url_for
from auth import login_is_required

routes_blueprint = Blueprint('routes_blueprint', __name__)

@routes_blueprint.route('/')
def index():
    return render_template('index.html')

@routes_blueprint.route('/dashboard')
@login_is_required
def dashboard():
    return render_template('dashboard.html')

@routes_blueprint.route('/show_items')
@login_is_required
def show_items():
    return render_template('show_items.html')

@routes_blueprint.route('/edit_items')
@login_is_required
def edit_items():
    return render_template('edit_items.html')

@routes_blueprint.route('/open_items')
@login_is_required
def open_items():
    return render_template('open_items.html')

@routes_blueprint.route('/save_links')
@login_is_required
def savelinks():
    return render_template('save_links.html')

@routes_blueprint.route('/settings')
@login_is_required
def settings():
    return render_template('settings.html')

@routes_blueprint.route('/summary')
@login_is_required
def summary():
    return render_template('summary.html')

@routes_blueprint.route('/user')
@login_is_required
def user():
    return "user page"

@routes_blueprint.route('/protected_area')
@login_is_required
def protected_area():
    # This is just a test. You can delete or use this. -Saugata
    return "<a href = '/logout'>Logout</a> <br><h4> Hello, your email is {} and <br> your name is {}.</h4>".format(session['email'], session['name'])

@routes_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect("/")
