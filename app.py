import os
from flask import Flask, render_template, request, session, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

app = Flask(__name__)

#db for local developement
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/db_dev'
db = SQLAlchemy(app)

#db for cloud
#heroku = Heroku(app)
#db = SQLAlchemy(app)

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

class Stone(db.Model):
    __tablename__ = 'stones'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    log_id = db.Column(db.Integer, db.ForeignKey('log.id'))

#Set homepage
@app.route('/index')
@app.route('/')
def index():
    """Render website's home page."""
    if 'user' in session:
        user_data = db.session.query(User).filter(User.id == session['user']['id']).first()
        return render_template('index.html',
                               user = session['user'],
                               logs = user_data.logs)
    else:
        return redirect(url_for('login')) #LOGIN AND REGISTER PAGE

#login and register
@app.route('/login')
def login():
    if 'error' in session:
        error = session.pop('error')
        return render_template('login.html', error = error)
    return render_template('login.html')

# Save e-mail to database
@app.route('/create_user', methods=['POST'])
def create_user():
    email = None
    error = None
    if request.method == 'POST':
        email = request.form['email']
        #check email does not exist
        if not db.session.query(User).filter(User.email == email).count():
            new_user = User(email)
            db.session.add(new_user)
            db.session.commit()
            #login_user(email)
            return redirect(url_for('index'))
        session['error'] = 'This e-mail is already assosciated with a user!'
        return redirect(url_for('login'))

@app.route('/validate_login', methods=['POST'])
def validate_login():
    email = request.form['email']
    try:
        user = db.session.query(User).filter(User.email == email).first()
        login_user(user)
        return redirect(url_for('index'))
    except:
        session['error'] = 'user does not exist'
        return redirect(url_for('login'))

@app.route('/add_log', methods=['POST'])
def add_log():
    new_log = Log(request.form['name'], session['user']['id'])
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def login_user(user):
    session['user'] = {'id':user.id,'nickname':user.nickname}
    session['logged_in'] = True

def logout_user():
    session.pop('user')
    session['logged_in'] = False

app.secret_key = 'YOU_WILL_NEVER_GEUSS'

if __name__ == '__main__':
    app.run(debug=True)
