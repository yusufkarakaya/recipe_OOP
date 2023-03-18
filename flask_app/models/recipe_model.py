from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class Recipe:
  DB = 'recipe_schema'
  def __init__(self, data):
    self.id = data['id']
    self.name = data['name']
    self.description = data['description']
    self.instruction = data['instruction']
    self.date = data['date']
    self.under_30 = data['under_30']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.creator = None
    self.all_recipes = []


  @classmethod
  def save(cls, data):
    query = """
            INSERT INTO recipes (user_id, name, description, instruction, date, under_30)
            VALUES (%(user_id)s, %(name)s, %(description)s, %(instruction)s, %(date)s, %(under_30)s);
            """
    return connectToMySQL(cls.DB).query_db(query,data)

    # select w/join (read all and read one)
  @classmethod
  def get_all_recipes(cls):
    query='''
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id;
        '''
    results = connectToMySQL( cls.DB ).query_db( query )
    if results:
      all_recipes = []
      for row in results:
          one_recipe=cls( row )

          user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': ' ',
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
          }
          one_recipe.creator = user_model.User( user_data )
          all_recipes.append( one_recipe )
      return all_recipes
    else:
      return []

  @classmethod
  def get_recipe_with_user(cls, data):
    query = """
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s;
            """
    results = connectToMySQL(cls.DB).query_db(query, data)
    recipe = cls (results[0])
    for row in results:
        user_data = {
          'id': row['users.id'],
          'first_name': row['first_name'],
          'last_name': row['last_name'],
          'email': row['email'],
          'password': ' ',
          'created_at': row['users.created_at'],
          'updated_at': row['users.updated_at']
        }
        recipe.creator = user_model.User( user_data )
        recipe.all_recipes.append( user_model.User( user_data ))
    return recipe

  @classmethod
  def get_recipe_by_id(cls, data):
    query = """
            SELECT * FROM recipes
            WHERE recipes.id = %(id)s
            """
    results = connectToMySQL(cls.DB).query_db(query, data)
    return results[0]

  @classmethod
  def update(cls, data):
    query = """
                UPDATE recipes SET 
                name = %(name)s,
                description = %(description)s,
                instruction = %(instruction)s,
                date = %(date)s,
                under_30 = %(under_30)s
                WHERE id = %(id)s
            """

    results = connectToMySQL(cls.DB).query_db(query,data)
    return results

  @classmethod
  def delete(cls, data):
    query = """
            DELETE FROM recipes WHERE id = %(id)s
            """
    return connectToMySQL(cls.DB).query_db(query,data)

  @staticmethod
  def valide_new_recipe(recipe):
    is_valid = True
    if len(recipe['name']) < 3:
        flash("Name must be at least 3 characters","create")
        is_valid = False
    if len(recipe['description']) < 3:
        flash("Last name must be at least 3 characters","create")
        is_valid = False
    if len(recipe['instruction']) <3 :
        flash("Instruction must be at least 3 characters","create")
        is_valid = False
    if len(recipe['date']) < 1 :
        flash("Date cannot be empty","create")
        is_valid = False

    return is_valid
