from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/register_form')
def register_form():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validation(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "phone_number": request.form['phone_number'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "about_me": request.form['about_me'],
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email", 'login')
        return redirect('/')
    elif not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/edit/<int:users_id>')
def edit_user(users_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': users_id
    }
    users = User.get_id(data)
    return render_template('edit.html', users=users)


@app.route('/update_user/<int:users_id>', methods=['POST'])
def update_user(users_id):
    if not User.edit_validation(request.form):
        return redirect(f"/edit/{users_id}")
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "phone_number": request.form['phone_number'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "about_me": request.form['about_me'],
    }
    User.update_user( data, users_id)
    return redirect('/profile')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
