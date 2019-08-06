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
    collection = mongo.db.meals
    meals = collection.find({})
    user_collection = mongo.db.user_items
    user_items = user_collection.find({})
    return render_template('profile.html', message= "", meals = meals, user_items = user_items)
    
@app.route('/add')

def add():
    # connect to the database
    meals = mongo.db.meals
    # insert new data
    # events.insert({"event":"First Day of Classes", "date":"2019-08-21"})
    # events.insert({"event":"Winter Break", "date":"2019-12-20"})
    # events.insert({"event":"Finals Begin", "date":"2019-12-01"})
    # events.insert({"event": "Madison's Birthday", "date":"2004-07-07"})
    # return a message to the user
    return "Event added"

@app.route('/meals/new', methods= ["GET", "POST"])

def meals_new():
    userdata = dict(request.form)
    meals = mongo.db.meals
    meals.insert(userdata)
    return redirect('/profile')
    
@app.route('/shopping', methods= ["GET", "POST"])

def shopping():
    collection = mongo.db.meals
    meals = collection.find({})
    user_collection = mongo.db.user_items
    user_items = user_collection.find({})
    items = mongo.db.items
    message1 = ""
    message2 = ""
    # items.insert({"item":"potatoes"})
    # items.insert({"item":"rice"})
    # items.insert({"item":"milk"})
    # items.insert({"item":"popcorn"})
    userdata = dict(request.form)
    existing_item = items.find_one({"item":request.form["item"]})
    user_collection.insert(userdata)
    if existing_item is None:
        message1 = ": This item is not in your supermarket!"
        return  render_template('profile.html', meals = meals, user_items = user_items, message1 = message1)
    else:
        message2 = ": This item is in your supermarket!"
        return  render_template('profile.html', meals = meals, user_items = user_items, message2 = message2)
        
    
    
    