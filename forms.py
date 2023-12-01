from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired



########### LOGIN FORM #############
class LoginForm(FlaskForm):
    userEmail = StringField('UserEmail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')




