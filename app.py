import os
from flask import Flask, render_template, request, session, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

app = Flask(__name__)

#db for local developement
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/sample_db'
db = SQLAlchemy(app)

#db for cloud
#heroku = Heroku(app)
#db = SQLAlchemy(app)

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
@app.route('/')
@app.route('/index')
@app.route('/')
def home():
    """Render website's home page."""
    if 'username' in session:
        user = User.query.filter_by(username=session["user_id"]).first()
        return render_template('index.html',
                               user = user)
    else:
        return render_template('login.html') #LOGIN AND REGISTER PAGE

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
            return render_template('index.html',
                                   user = email)
        error = 'This e-mail is already assosciated with a user!'
        return render_template('login.html',
                               registration_error = error)

@app.route('/validate_login', methods=['POST'])
def validate_login():
    email = request.form['email']
    if db.session.query(User).filter(User.email == email).count():
        return render_template('index.html',
                               user = email)

if __name__ == '__main__':
    app.run(debug=True)
