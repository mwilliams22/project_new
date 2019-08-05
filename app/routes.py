import os
from app import app
from flask import render_template, request, redirect, session, url_for 

from flask_pymongo import PyMongo

app.secret_key = b'\x1b\xe3)\x89Hz\x83X\xb6\xe2\xdb\x17\xa1J\x94J'

# name of database
app.config['MONGO_DBNAME'] = 'database' 

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:Purple123@cluster0-3obbt.mongodb.net/database?retryWrites=true&w=majority' 

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])

def signup():
    if request.method == 'POST':
        #take in info, check if username is taken, if it is available, put in database of users
        users = mongo.db.project_users
        existing_user = users.find_one({"username":request.form['username']})
        if existing_user is None:
            users.insert({"username":request.form['username'], "password":request.form['password']})
            return redirect(url_for('market'))
        else:
            message = "That username is taken. Try logging in or try a different username."
            return render_template('signup.html', message = message)
    else:
        return render_template('signup.html', message = "")
        
@app.route('/market', methods = ["POST", "GET"])

def market():
    if request.method == "GET":
        return render_template('market.html')
    else:
        message = "Your supermarket has been saved"
        return render_template('profile1.html', message = message)
        
@app.route('/login', methods= ["POST", "GET"])

def login():
    if request.method == 'POST':
        users = mongo.db.project_users
        #use the username to find the account
        existing_user = users.find_one({"username":request.form["username"]})
        if existing_user:
            #check if the password is right
            if existing_user['password'] == request.form["password"] :
                session['username'] = request.form['username']
                return redirect(url_for('profile'))
            else:
                message = "Your password doesn't match your username.Try again."
                return render_template('login.html', message = message)
        else:
            message = "There is no user with that username. Try making an account."
            return render_template('signup.html', message = message)
    else:
        return render_template('login.html', message = "")

# lOG OUT
@app.route('/logout')

def logout():
    session.clear()
    return redirect('/')

@app.route('/profile', methods = ["POST", "GET"])

def profile():
    return render_template('profile.html', message= "")

@app.route('/meals/new', methods= ["GET", "POST"])

def meals_new():
    userdata = dict(request.form)
    meals = mongo.db.meals
    meals.insert(userdata)
    return render_template('profile.html')
    
@app.route('/shopping', methods= ["GET", "POST"])

def shopping():
    userdata = dict(request.form)
    meals 