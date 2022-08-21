from flask_app import app
from flask import flash, render_template, redirect, request, session, url_for
#Models
from flask_app.models.woodproject import Woodproject
from flask_app.models.user import User
#Image upload: 
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.path.abspath('../the_woodworking_joint/flask_app/static/user_img/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


###################################### 
# HOME ROUTE
###################################### 

@app.route('/')
def index():
    return render_template('index.html')


###################################### 
# VIEW - DASHBOARD
###################################### 

#View all projects
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_one_by_id(data), woodprojects=Woodproject.get_all())


#View projects created by self
@app.route('/dashboard/myprojects')
def mywoodprojects():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = {
        "user_id":session['user_id'],#user_id is the foreign key within woodprojects
        "id":session['user_id'] #id is for the user query
    }
    return render_template("dashboard.html", woodprojects=Woodproject.get_all_by_one_user(user_id), user=User.get_one_by_id(user_id))


#View favorited projectes
@app.route('/dashboard/myfavorites')
def myfavoritewoodprojects():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = {
        "user_id":session['user_id'],#user_id is the foreign key within woodprojects
        "id":session['user_id'] #id is for the user query
    }
    return render_template("dashboard.html", woodprojects=Woodproject.get_all_favorites_by_one_user(user_id), user=User.get_one_by_id(user_id))


#View filtered projects based on search
@app.route('/dashboard/mysearch')
def mysearch():
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = {
        "user_id":session['user_id'],#user_id is the foreign key within woodprojects
        "id":session['user_id'] #id is for the user query
    }
    data = {
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
    }
    return render_template("dashboard.html", woodprojects=Woodproject.get_all_woodprojects_by_user_search(data), user=User.get_one_by_id(user_id))


###################################### 
# VIEW - ONE
###################################### 

@app.route('/woodproject/<int:id>')
def woodproject(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view.html", woodproject=Woodproject.get_one_woodproject_by_id(data), user=User.get_one_by_id(user_data))


###################################### 
# FAVORITING
###################################### 
@app.route('/favorite/<int:woodproject_id>/<int:user_id>')
def add_favorite(user_id, woodproject_id):
    data = {
        "woodproject_id": woodproject_id,
        "user_id": user_id
    }
    Woodproject.add_favorite(data)
    print("REQUEST.REFERRER", request.referrer)
    return redirect(f"{request.referrer}#{woodproject_id}")

@app.route('/unfavorite/<int:woodproject_id>/<int:user_id>')
def remove_favorite(user_id, woodproject_id):
    data = {
        "woodproject_id": woodproject_id,
        "user_id": user_id
    }
    Woodproject.destroy_favorite(data)
    print("REQUEST.REFERRER", request.referrer)
    return redirect(f"{request.referrer}#{woodproject_id}")




###################################### 
# CREATE & SAVE 
###################################### 

@app.route('/new')
def new():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("create.html",user=User.get_one_by_id(data))


@app.route('/create/woodproject', methods=['POST']) 
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Woodproject.validate_woodproject_form(request.form):
        if not Woodproject.validate_woodproject_image(request.files):
            return redirect('/new')
    #Creates the file variable connected to the HTML 
    file = request.files['woodProjectImg']
    if file:
        filename = secure_filename(file.filename)
        image_path = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("IMAGE VALIDATION - File saved here:", image_path)
    #Saves the form and the image's path to the db
    data = {
        "project_name": request.form["project_name"],
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
        "description": request.form["description"],
        "image_path" : image_path,
        "user_id": session["user_id"]
    }
    Woodproject.save(data)
    return redirect('/dashboard')


###################################### 
# UPDATE 
###################################### 

@app.route('/edit/<int:id>')
def edit_form(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id #woodproject's ID
    } 
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html", woodproject=Woodproject.get_one_woodproject_by_id(data), user=User.get_one_by_id(user_data))


@app.route('/update/woodproject',methods=['POST'])
def update_form():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Woodproject.validate_woodproject_form(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    data = {
        "project_name": request.form["project_name"],
        "skill_level": request.form["skill_level"],
        "type": request.form["type"],
        "description": request.form["description"],
        "id": request.form["id"]
    }
    Woodproject.update_form(data)
    return redirect(f'/woodproject/{request.form["id"]}')


@app.route('/edit/<int:id>/image')
def edit_image(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id #woodproject's ID
    } 
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_image.html", woodproject=Woodproject.get_one_woodproject_by_id(data), user=User.get_one_by_id(user_data))


@app.route('/update/woodproject/image', methods=['POST']) 
def update_image():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Woodproject.validate_woodproject_image(request.files): 
        return redirect(f'/edit/{request.form["id"]}/image')
    #Creates the file variable connected to the HTML 
    file = request.files['woodProjectImg']
    print("FILE = REQUEST.FILES", file)
    if file:
        filename = secure_filename(file.filename)
        image_path = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("IMAGE VALIDATION - File saved here:", image_path)
    #Saves the form and the image's path to the db
    data = {
        "image_path" : image_path,
        "id": request.form["id"]
    }
    Woodproject.update_image(data)
    # return redirect('/dashboard')
    return redirect(f'/edit/{request.form["id"]}')


###################################### 
# DELETE 
###################################### 

@app.route('/destroy/woodproject/<int:id>')
def destory(id):
    if 'user_id' not in session:
        return redirect('logout')
    data = {
        "id":id
    }
    Woodproject.destroy(data)
    return redirect("/dashboard")

