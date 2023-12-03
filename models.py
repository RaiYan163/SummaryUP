from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    userID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=True)
    lastName = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    # Relationships
    summaries = db.relationship('Summary', backref='user', lazy='dynamic')
    saved_links = db.relationship('SavedLink', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def get_id(self):
        return str(self.userID)

class Summary(db.Model):
    __tablename__ = 'Summary'
    summaryID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'), nullable=True)
    summaryTitle = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    summaryBody = db.Column(db.Text, nullable=True) 
    summaryLink = db.Column(db.String(255), nullable=True)

class SavedLink(db.Model):
    __tablename__ = 'SavedLink'
    linkID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('User.userID'), nullable=True)
    linkTitle = db.Column(db.String(255), nullable=True)
    linkDescription = db.Column(db.String(255), nullable=True)
    linkURL = db.Column(db.String(255), nullable=True)
    linkCategory = db.Column(db.String(255), nullable=True)

class Admin(UserMixin, db.Model):
    __tablename__ = 'Admin'
    adminID = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

    def get_id(self):
        return str(self.adminID)
