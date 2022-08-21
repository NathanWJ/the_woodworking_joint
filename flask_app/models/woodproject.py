from multiprocessing import allow_connection_pickling
from operator import truediv
from sqlite3 import connect
from unittest import result
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
#Image upload and validation: 
import os
from werkzeug.utils import secure_filename
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg'} #


class Woodproject:
    db = "woodworking_joint"
    def __init__(self,data):
        self.id = data['id']
        self.project_name = data['project_name']
        self.skill_level = data['skill_level']
        self.type = data['type']
        self.description = data['description']
        self.image_path = data['image_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None #Gets User object
        self.favorited_by = set() #for number of favs, can just use len({instance}.like_by)


###################################### 
# VIEW - DASHBOARD
###################################### 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM woodprojects LEFT JOIN favorites on woodprojects.id = favorites.woodproject_id;"
        results = connectToMySQL(cls.db).query_db(query)
        project_ids = set()
        projects = []
        for i in range(len(results)):
            this_id = results[i]["id"]
            user_id = results[i]["favorites.user_id"]
            if this_id not in project_ids: #only create an object if not already done
                project_ids.add(this_id) # Keep track of the projects we've found
                project = cls(results[i])
                if user_id: #check if this exists
                    project.favorited_by.add(user_id) # add the id of the user that liked it
                projects.append(project)
            else: #we've already found this proejct previously
                if projects[-1].id == this_id: #This row likely references the same project in the last row
                    ref_idx = len(projects) - 1
                else: 
                    for x in range(len(projects)): #brute force search otherwise
                        if projects[x].id == this_id:
                            ref_idx = xbreak
                if user_id:
                    projects[ref_idx].favorited_by.add(user_id) #we don't want to add a new project, but we do want to add to its liked by
        return projects

    @classmethod
    def get_all_by_one_user(cls,data):
        query = "SELECT * FROM woodprojects LEFT JOIN favorites on woodprojects.id = favorites.woodproject_id WHERE woodprojects.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        project_ids = set()
        projects = []
        for i in range(len(results)):
            this_id = results[i]["id"]
            user_id = results[i]["favorites.user_id"]
            if this_id not in project_ids: #only create an object if not already done
                project_ids.add(this_id) # Keep track of the projects we've found
                project = cls(results[i])
                if user_id: #check if this exists
                    project.favorited_by.add(user_id) # add the id of the user that liked it
                projects.append(project)
            else: #we've already foudn this proejct previously
                if projects[-1].id == this_id: #This row likely references the same project in the last row
                    ref_idx = len(projects) - 1
                else: 
                    for x in range(len(projects)): #brute force search otherwise
                        if projects[x].id == this_id:
                            ref_idx = xbreak
                if user_id:
                    projects[ref_idx].favorited_by.add(user_id) #we don't want to add a new project, but we do want to add to its liked by
        return projects


    @classmethod
    def get_all_favorites_by_one_user(cls,data):
        query = "SELECT * FROM woodprojects LEFT JOIN favorites on woodprojects.id = favorites.woodproject_id WHERE favorites.user_id= %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        project_ids = set()
        projects = []
        for i in range(len(results)):
            this_id = results[i]["id"]
            user_id = results[i]["favorites.user_id"]
            if this_id not in project_ids: #only create an object if not already done
                project_ids.add(this_id) # Keep track of the projects we've found
                project = cls(results[i])
                if user_id: #check if this exists
                    project.favorited_by.add(user_id) # add the id of the user that liked it
                projects.append(project)
            else: #we've already foudn this proejct previously
                if projects[-1].id == this_id: #This row likely references the same project in the last row
                    ref_idx = len(projects) - 1
                else: 
                    for x in range(len(projects)): #brute force search otherwise
                        if projects[x].id == this_id:
                            ref_idx = xbreak
                if user_id:
                    projects[ref_idx].favorited_by.add(user_id) #we don't want to add a new project, but we do want to add to its liked by
        return projects


###################################### 
# VIEW - ONE
###################################### 

    @classmethod
    def get_one_woodproject_by_id(cls,data):
        query = "SELECT * FROM woodprojects LEFT JOIN users ON woodprojects.user_id = users.id WHERE woodprojects.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        one_woodproject = cls(results[0]) #Creates a Woodproject Object as an instance of the class
        user_data = {
            "id" : results[0]["users.id"],
            "username" : results[0]["username"],
            "email" : "hidden",
            "password" : "hidden",
            "created_at" : "hidden",
            "updated_at" :"hidden"
        }
        one_user = user.User(user_data) #Instantiates the user from the query based on the User class
        one_woodproject.user = one_user
        return one_woodproject


###################################### 
# FAVORITE
###################################### 

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favorites (woodproject_id,user_id) VALUES (%(woodproject_id)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data);


    @classmethod
    def destroy_favorite(cls,data):
        query = "DELETE FROM favorites WHERE user_id=%(user_id)s AND woodproject_id=%(woodproject_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# CREATE & SAVE
###################################### 

    @classmethod
    def save(cls, data):
        query = "INSERT INTO woodprojects (project_name, skill_level, type, description, image_path, user_id) VALUES (%(project_name)s, %(skill_level)s, %(type)s, %(description)s, %(image_path)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# UPDATE 
###################################### 
    @classmethod
    def update_form(cls,data):
        query = "UPDATE woodprojects SET project_name=%(project_name)s,skill_level=%(skill_level)s,type=%(type)s,description=%(description)s,updated_at=NOW() WHERE id=%(id)s;"
        print(query)
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update_image(cls,data):
        query = "UPDATE woodprojects SET image_path=%(image_path)s,updated_at=NOW() WHERE id=%(id)s;"
        print(query)
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# DELETE 
###################################### 

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM woodprojects WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


###################################### 
# VALIDATION METHODS 
######################################

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS


    @staticmethod
    def validate_woodproject_form(woodproject):
        is_valid = True
        if len(woodproject['project_name']) < 3:
            is_valid = False
            flash("Project name must be at least 3 characters","project_name")
        if "skill_level" not in woodproject:
            is_valid = False
            flash("Please select a skill level","skill_level")
        if "type" not in woodproject:
            is_valid = False
            flash("Please select a type","type")
        if len(woodproject['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","description")
        return is_valid


    @staticmethod
    def validate_woodproject_image(woodimage):
        #Reference: https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
        is_valid = True
        file = woodimage['woodProjectImg'] 
        if file.filename == '':
            flash("No image selected. Please choose an image.", "image_path")
            print("IMAGE VALIDATION - No file selected. Blank field.")
            is_valid = False
        elif not Woodproject.allowed_file(file.filename):
            flash("Image must be a png, jpg, or jpeg file type.", "image_path")
            print("IMAGE VALIDATION - File type extension is invalid.")
            is_valid = False
        return is_valid
