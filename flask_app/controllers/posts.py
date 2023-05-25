from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.config.mysqlconnection import connectToMySQL

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_id(data)
    post = Post.get_all_likes()
    return render_template('dashboard.html', user=user, post=post)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id':session['user_id']
    }
    users = User.get_id(user_data)
    return render_template('profile.html', users=users)

@app.route('/post')
def post():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    user = User.get_id(data)
    return render_template('post.html', user=user)

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'country': request.form['country'],
        'city': request.form['city'],
        'recommendation': request.form['recommendation'],
        'info': request.form['info'], 
        'user_id': session['user_id']
    }
    if not Post.post_validation(request.form):
        return redirect('post')
    Post.save(data)
    return redirect('/dashboard')

@app.route('/like/<int:post_id>')
def like(post_id):
    data = {
        'post_id': post_id,
        'user_id': session['user_id']
    }
    Post.like(data)
    return redirect('/dashboard')

@app.route('/dislike/<int:post_id>')
def dislike(post_id):
    data = {
        'post_id': post_id,
        'user_id': session['user_id']
    }
    Post.dislike(data)
    return redirect('/dashboard')

@app.route('/connect')
def connect():
    if 'user_id' not in session:
        return redirect('/')
    users = User.get_all()
    return render_template('connect.html', users=users)


@app.route('/comment/<int:post_id>')
def comment(post_id):
    if 'user_id' not in session:
        return redirect('/')
    user_data ={
        'id': session['user_id']
    }
    users = User.get_id(user_data)
    return render_template('comment.html', users=users, post_id=post_id)

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'comment_data': request.form['comment_data'],
        'users_id': session['user_id'],
        'posts_id': post_id
    }
    post = Post.save_comment(data)
    return redirect('/dashboard')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    data = {
        'id': post_id
    }
    Post.delete(data)
    return redirect('/dashboard')

