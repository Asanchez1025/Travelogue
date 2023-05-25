from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
db = 'travelogue'


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.country = data['country']
        self.city = data['city']
        self.recommendation = data['recommendation']
        self.info = data['info']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.all_user_likes =[]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts(country, city, recommendation, info, user_id) VALUES(%(country)s, %(city)s, %(recommendation)s, %(info)s, %(user_id)s)"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def save_comment(cls, data):
        query = "INSERT INTO comments(comment_data, users_id, posts_id)  VALUES(%(comment_data)s, %(users_id)s, %(posts_id)s)"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def save_pic(cls, data):
        query = "INSERT INTO posts(picture) VALUES(%(picture)s)"
        return connectToMySQL(db).query_db(query, data)

    """ @classmethod
    def get_all_users_posts(cls, data):
        query = "SELECT * FROM posts JOIN users ON users.id = posts.user_id WHERE posts.id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        posts = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'phone_number': results[0]['phone_number'],
                'password': results[0]['password'],
                'about_me': results[0]['about_me'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at'],
        }
        posts.user = User(user_data)
        return posts """
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts"
        results = connectToMySQL(db).query_db(query)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts

    @ classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes(users_id, posts_id) VALUES (%(user_id)s, %(post_id)s)"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def dislike(cls, data):
        query = "DELETE from likes WHERE posts_id =%(post_id)s AND users_id =%(user_id)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_likes(cls):
        query = "SELECT * FROM posts JOIN users On users.id = posts.user_id LEFT JOIN likes ON posts.id = likes.posts_id LEFT JOIN users AS users2 ON users2.id = likes.users_id"
        results = connectToMySQL(db).query_db(query)
        likes = []
        for result in results:
            new_like = True
            liked_user_data = {
                'id': result['users2.id'],
                'first_name': result['users2.first_name'],
                'last_name': result['users2.last_name'],
                'email': result['users2.email'],
                'phone_number': result['users2.phone_number'],
                'password': result['users2.password'],
                'about_me': result['users2.about_me'],
                'created_at': result['users2.created_at'],
                'updated_at': result['users2.updated_at'],
            }
            if len(likes) > 0 and likes[len(likes)-1].id ==result['id']:
                likes[len(likes)-1].all_user_likes.append(User(liked_user_data))
                new_like = False
            if new_like:
                like = cls(result)
                user_data = {
                    'id': result['users.id'],
                    'first_name': result['first_name'],
                    'last_name': result['last_name'],
                    'email': result['email'],
                    'phone_number': result['phone_number'],
                    'password': result['password'],
                    'about_me': result['about_me'],
                    'created_at': result['users.created_at'],
                    'updated_at': result['users.updated_at'],
                }
                user = User(user_data)
                like.user = user
                if result['users2.id'] is not None:
                    like.all_user_likes.append(User(liked_user_data))
                likes.append(like)
        return likes

    @staticmethod
    def post_validation(post):
        is_valid = True
        if len(post['country']) < 2:
            flash('You must enter a valid Country', "post_error" )
            is_valid = False
        if len(post['city']) < 2:
            flash('You must enter a valid City', "post_error" )
            is_valid = False
        if len(post['recommendation']) < 3:
            flash('You must enter a valid comment', "post_error" )
            is_valid = False
        if len(post['info']) < 2:
            flash('You must enter valid info', "post_error" )
            is_valid = False
        return is_valid
