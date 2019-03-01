#!/usr/bin/python
import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import pickle

### WEB APP ###
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///WouldU.db")

@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    # Create form
    form = ReusableForm(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # Extract information
        seed = request.form['seed']
        diversity = float(request.form['diversity'])
        words = int(request.form['words'])
        # Generate a random sequence
        if seed == 'random':
            return render_template('random.html',
                                   input=generate_random_start(model=model,
                                                               graph=graph,
                                                               new_words=words,
                                                               diversity=diversity))
        # Generate starting from a seed sequence
        else:
            return render_template('seeded.html',
                                   input=generate_from_seed(model=model,
                                                            graph=graph,
                                                            seed=seed,
                                                            new_words=words,
                                                            diversity=diversity))
    # Send template information to index.html
    return render_template('index.html', form=form)

loaded_model = pickle.load(open("facebookModel.sav", "rb"))
# result = loaded_model.predict(np.expand_dims(userData, axis=1).T)

#
# @app.route("/create", methods=["GET", "POST"])
# def create(phraseList=phraseList, scoresList=scoresList):
# 	if request.method == 'POST':
# 		# ensure first name isnt blank
# 		if not request.form.get('newPhrase'):
# 			return render_template("homepage.html")
# 		else:
# 			phraseList, scoresList = create_new(phraseList=phraseList, scoresList=scoresList, newPhrase=request.form.get('newPhrase'))
# 			print("Created!")
# 			print(phraseList, scoresList)
# 			return render_template('create.html')
# 	else:
# 		return render_template('create.html')
#
# @app.route("/leaderboards")
# def leaderboards():
# 	return render_template('leaderboards.html')
#
# @app.route("/register", methods=["GET", "POST"])
# def register():
# 	if request.method == 'POST':
# 		print("post")
# 	else:
# 		return render_template('register.html')

from wtforms import (Form, TextField, validators, SubmitField,
DecimalField, IntegerField)

class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    # Starting seed
    seed = TextField("Enter a seed string or 'random':", validators=[
                     validators.InputRequired()])
    # Diversity of predictions
    diversity = DecimalField('Enter diversity:', default=0.8,
                             validators=[validators.InputRequired(),
                                         validators.NumberRange(min=0.5, max=5.0,
                                         message='Diversity must be between 0.5 and 5.')])
    # Number of words
    words = IntegerField('Enter number of words to generate:',
                         default=50, validators=[validators.InputRequired(),
                                                 validators.NumberRange(min=10, max=100,
                                                 message='Number of words must be between 10 and 100')])
    # Submit button
    submit = SubmitField("Enter")
