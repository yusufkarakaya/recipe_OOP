from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user_model
from flask_app.models import recipe_model
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = user_model.User.get_by_id(data)
    recipes = recipe_model.Recipe.get_all_recipes()
    return render_template("recipes.html", user = user, recipes = recipes)

@app.route('/recipes/new')
def create_recipe():
  if 'user_id' not in session:
      return redirect('/logout')
  return render_template('create_recipe.html')

@app.route('/recipe/<int:id>')
def view(id):
  id_data = {
    "id" : id
  }
  data = {
        'id': session['user_id']
  }
  return render_template('/one_recipe.html', recipe_with_user = recipe_model.Recipe.get_recipe_with_user(id_data), user = user_model.User.get_by_id(data))

@app.route('/create_recipe', methods=['POST'])
def create():
  if not recipe_model.Recipe.valide_new_recipe(request.form):
    return redirect('/recipes/new')

  recipe_model.Recipe.save(request.form)
  return redirect('/recipes')

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
  id_data = {
    "id" : id
  }
  recipes = recipe_model.Recipe.get_recipe_by_id(id_data)
  return render_template("/edit_recipe.html", recipes = recipes)

@app.route('/update_recipe', methods=['POST'])
def update():
  print(request.form)
  recipe_model.Recipe.update(request.form)
  return redirect('/recipes')


@app.route('/delete/<int:id>')
def delete_recipe(id):
  id_data = {
    "id" : id
  }
  recipe_model.Recipe.delete(id_data)
  return redirect('/recipes')