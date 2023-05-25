from flask_app.config.mysqlconnection import connectToMySQL
db = 'travelogue'

class File:
    def __init__(self, file_dict):
        self.id = file_dict['id'],
        self.file_name = file_dict['file_name'],
        self.size = file_dict['size'],
        self.size = file_dict['size'],
        self.extension = file_dict['extension'],
        self.users_id = file_dict['users_id'],
        self.created_at = file_dict['created_at'],
        self.updated_at = file_dict['updated_at'],

    @classmethod
    def save(cls, data):
        query = "INSERT INTO file(file_name, size, extension, users_id) VALUES(%(file_name)s, %(size)s, %(extension)s, %(users_id)s)"
        return connectToMySQL(db).query_db(query, data)