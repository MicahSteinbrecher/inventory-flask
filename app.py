import os
from flask import Flask, render_template, request, session, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

app = Flask(__name__)

#db for local developement
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/sample_db'
#db = SQLAlchemy(app)

#db for cloud
heroku = Heroku(app)
db = SQLAlchemy(app)

#Create db model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

#Set homepage
@app.route('/index')
@app.route('/')
def index():
    """Render website's home page."""
    if 'user' in session:
        return render_template('index.html',
                               user = session['user'])
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
            login_user(email)
            return redirect(url_for('index'))
        session['error'] = 'This e-mail is already assosciated with a user!'
        return redirect(url_for('login'))

@app.route('/validate_login', methods=['POST'])
def validate_login():
    email = request.form['email']
    if db.session.query(User).filter(User.email == email).count():
        login_user(email)
        return redirect(url_for('index'))
    session['error'] = 'user does not exist'
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def login_user(user):
    session['user'] = user
    session['logged_in'] = True

def logout_user():
    session.pop('user')
    session['logged_in'] = False

app.secret_key = 'YOU_WILL_NEVER_GEUSS'

if __name__ == '__main__':
    app.run(debug=True)
