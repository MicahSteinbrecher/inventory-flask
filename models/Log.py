from config import app, db

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stones =db.relationship ('Stone', backref='stone', lazy = 'dynamic')
    value = db.Column(db.Float)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id