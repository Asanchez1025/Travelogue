from flask_app.config.mysqlconnection import connectToMySQL
db = 'travelogue'

class File:
    def __init__(self, comment_dict):
        self.comment_data = comment_dict['comment_data'],
        self.users_id = comment_dict['users_id'],
        self.posts_id = comment_dict['posts_id'],

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments(comment_data, users_id, posts_id) VALUES(%(comment_data)s, %(users_id)s, %(posts_id)s)"
        return connectToMySQL(db).query_db(query, data)