import os
from app import app
from flask import render_template, request, redirect

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
            return "User saved"
        else:
            message = "That username is taken. Try logging in or try a different username."
            return render_template('signup.html', message = message)
    else:
        return render_template('signup.html', message = '')
        
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
                return redirect(url_for('index'))
            else:
                return "Your password doesn't match your username."
        else:
            return "There is no user with that username. Try making an account."
    else:
        return render_template('login.html', message = '')
