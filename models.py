from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash

######### User Model #############
class User(UserMixin, db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    password= db.Column(db.String(255))
    avatar = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    age = db.Column(db.Integer)

    summaries = db.relationship('Summary', backref='user', lazy=True)
    saved_links = db.relationship('SavedLink', backref='user', lazy=True)

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def get_id(self):
        return str(self.userID)

class Summary(db.Model):
    summaryID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    urlLink = db.Column(db.String(255))
    summaryTitle = db.Column(db.String(255))
    rating = db.Column(db.Integer)

class SavedLink(db.Model):
    linkID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    linkTitle = db.Column(db.String(255))
    linkDescription = db.Column(db.String(255))
    linkURL = db.Column(db.String(255))
    linkCategory = db.Column(db.String(255))

class Admin(db.Model):
    adminID = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(255))
    password = db.Column(db.String(255))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))