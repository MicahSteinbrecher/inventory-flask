import os
from flask import Flask, render_template, request, session, redirect, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from models.User import User
from models.Log import Log
from models.Stone import Stone
from config import app, db
from Rapaport.diamond import Diamond

#Set homepage
@app.route('/index/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    """Render website's home page."""
    if 'user' in session:
        user_data = db.session.query(User).filter(User.id == session['user']['id']).first()
        if request.method == 'POST':
            session["current_log_id"] = request.form['log_id']
        if 'current_log_id' in session:
            current_log = db.session.query(Log).filter(Log.id == session['current_log_id']).first()
            diamonds = change_to_diamonds(current_log.stones)
            return render_template('index.html',
                                   user = session['user'],
                                   logs = user_data.logs,
                                   current_log = current_log.name,
                                   diamonds = diamonds)
        else:
            return render_template('index.html',
                               user = session['user'],
                               logs = user_data.logs)
    else:
        return redirect(url_for('login')) #LOGIN AND REGISTER PAGE

def change_to_diamonds(stones):
    diamonds = []
    for stone in stones:
        diamond = Diamond()
        diamond.set_clarity(stone.clarity)
        diamond.set_color(stone.color)
        diamond.set_size(stone.size)
        diamond.set_shape('round')
        diamond.value = diamond.get_carat_price(os.environ['RAPAPORT_USERNAME'], os.environ['RAPAPORT_PASSWORD']) * stone.size
        diamond.set_shape(stone.shape)
        diamonds.append(diamond)
    return diamonds

def get_rapaport_shape(shape):
    if shape == 'oval' or shape == 'marquise' or shape == 'heart' or shape == 'pear':
        return 'oval'
    else:
        return 'round'


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
            login_user(db.session.query(User).filter(User.email == email).first())
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

#log_id, shape, color, clarity, size
@app.route('/add_stone', methods=['POST'])
def add_stone():
    new_stone = Stone(request.form['shape'], request.form['color'], request.form['clarity'], request.form['size'])
    db.session.add(new_stone)
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
    session.clear()

app.secret_key = 'YOU_WILL_NEVER_GEUSS'

if __name__ == '__main__':
    app.run(debug=True)
