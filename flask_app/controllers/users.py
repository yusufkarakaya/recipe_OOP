from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user_model
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def users():
  return render_template('index.html')

@app.route('/register', methods= ['POST'])
def register_user():
  if not user_model.User.validate_register(request.form):
    return redirect('/')
    
  user_model.User.save_user(request.form)
  return redirect('/recipes')

@app.route('/login', methods=['POST'])
def login():
  if not user_model.User.validate_login(request.form):
    return redirect('/')
  email_data = {
    'email':request.form['login-email']
  }
  returning_user= user_model.User.get_user_by_email(email_data)
  session['user_id']= returning_user.id
  return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
