from config import app, db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    nickname = db.Column(db.String(120))
    logs = db.relationship('Log', backref='user', lazy = 'dynamic')
    stones = db.relationship('Stone', backref='user', lazy = 'dynamic')
    '''
    want to have option to initialize with a proper nickname,
    and if no nickname is passed, do nickname = email
    '''
    def __init__(self, email):
        self.email = email
        self.nickname = email

    def __repr__(self):
        return '<User %r>' % self.email