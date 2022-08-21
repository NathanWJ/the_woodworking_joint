from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import woodproject
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db = "woodworking_joint"
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.woodprojects = []
        self.favorit_woodprojects = []




###################################### 
# FAVORITE
###################################### 
    @classmethod
    def get_favorite_projects(cls,data):
        query = "SELECT * FROM favorites WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        favorited_projects = []
        for i in results:
            favorited_projects.append(i['woodproject_id'])
        return favorited_projects



###################################### 
# CREATE METHODS 
###################################### 

    @classmethod
    def save(cls, data):
        query="INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# READ METHODS 
###################################### 

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data) 
        return cls(results[0]) 

    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])


###################################### 
# UPDATE METHODS 
###################################### 

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET username=%(username)s,email=%(email)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

###################################### 
# DELETE METHODS 
###################################### 

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# VALIDATION AT REGISTRATION
###################################### 

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db).query_db(query,user)
        if len(user['username']) < 2:
            flash("Username must be at least 2 characters.","username")
            is_valid = False

        if len(result) >= 1:
            flash("Email already taken.","email")
            is_valid = False
        elif len(user['email']) <1:
            flash("Please add an email.","email")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email. Please try again.","email")
            is_valid = False

        if len(user['password']) < 1:
            flash("Password can't be blank.","password")
            is_valid = False
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters.","password")
            is_valid = False

        if len(user['password_confirmation']) < 1:
            flash("Password can't be blank.","password_confirmation")
            is_valid = False
        elif user['password'] != user['password_confirmation']:
            flash("Passwords do not match. Please try again.","password_confirmation")
            is_valid = False
        return is_valid

