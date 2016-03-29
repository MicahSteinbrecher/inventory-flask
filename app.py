import os
from flask import Flask, render_template, request
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
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('index.html')

# Save e-mail to database
@app.route('/register', methods=['POST'])
def register():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        #check email does not exist
        if not db.session.query(User).filter(User.email == email).count():
            new_user = User(email)
            db.session.add(new_user)
            db.session.commit()
            return render_template('index.html')
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
