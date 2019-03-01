#!/usr/bin/python
import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

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

@app.route("/")
def index():
	return render_template('index.html')
    
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
