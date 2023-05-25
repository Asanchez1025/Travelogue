from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'travelogue'


class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.phone_number = data['phone_number']
        self.password = data['password']
        self.about_me = data['about_me']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, phone_number, password, about_me) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(phone_number)s,%(password)s, %(about_me)s)"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def update_user(cls, form_data, users_id):
        query = f"UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email =%(email)s, phone_number = %(phone_number)s, password = %(password)s, about_me = %(about_me)s WHERE id = {users_id};"
        return connectToMySQL(db).query_db(query, form_data)


    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @staticmethod
    def validation(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if len(user['phone_number']) < 10:
            flash("Must enter a valid Phone number", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match!!")
            is_valid = False
        return is_valid


    @staticmethod
    def edit_validation(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, user)
        if len(results) >= 1:
            flash("Must have a valid email.", "edit_error")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "edit_error")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters", "edit_error")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "edit_error")
            is_valid = False
        if len(user['phone_number']) < 10:
            flash("Must enter a valid Phone number", "edit_error")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "edit_error")
            is_valid = False
        return is_valid