from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.wine import Wine
from flask_app.models.user import User

@app.route('/new')
def new_wine():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template('new_wine.html',user=User.get_by_id(data))

@app.route('/create/wine',methods=['POST'])
def create_wine():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Wine.validate_wine(request.form):
        return redirect('/new')
    data = {
        "name": request.form["name"],
        "type": request.form["type"],
        "description": request.form["description"],
        "price": request.form["price"],
        "user_id": session['user_id']
    }
    Wine.save(data)
    return redirect('/dashboard')

@app.route('/edit/wine/<int:id>')
def edit_wine(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",edit=Wine.get_one(data),user=User.get_by_id(user_data))


@app.route('/update/wine/<int:id>',methods=['POST'])
def update_wine(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Wine.validate_wine(request.form):
        return redirect(f'/edit/wine/{id}')
    data = {
        "name": request.form["name"],
        "type": request.form["type"],
        "description": request.form["description"],
        "price": request.form["price"],
        "id": request.form['id']
    }
    Wine.update(data)
    return redirect('/dashboard')

@app.route('/show')
def show_wines():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_wine.html",wine=Wine.get_all(),user=User.get_by_id(user_data))

@app.route('/show/<int:id>')
def show_wine(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_wine.html",wine=Wine.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/wine/<int:id>')
def destroy_wine(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Wine.destroy(data)
    return redirect('/dashboard')

@app.route('/purchase')
def purchase():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template("purchase.html",wine=Wine.get_all(),user=User.get_by_id(user_data))

@app.route('/favorites/wine/<int:id>')
def favorite_wine(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":session['user_id'],
        "wine_id":id
    }
    Wine.favorites(data)
    return redirect('/show')

@app.route('/unfavorites/wine/<int:id>')
def unfavorite_wine(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":session['user_id'],
        "wine_id":id
    }
    Wine.unfavorites(data)
    return redirect('/show')
