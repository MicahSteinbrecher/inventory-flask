from config import app, db
from flask import session

class Stone(db.Model):
    __tablename__ = 'stones'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    log_id = db.Column(db.Integer, db.ForeignKey('log.id'))
    shape = db.Column(db.String(20))
    color = db.Column(db.String(20))
    clarity = db.Column(db.String(20))
    size = db.Column(db.Float)
    value = db.Column(db.Float)

    def __str__(self):
        str = 'shape: %s, color: %s, clarity: %s, size, %s' % (self.shape, self.color, self.clarity, self.size)
        return str

    def __init__(self, shape, color, clarity, size):
        self.user_id = session['user']['id']
        self.log_id = session['current_log_id']
        self.shape = shape
        self.color = color
        self.clarity = clarity
        self.size = size
