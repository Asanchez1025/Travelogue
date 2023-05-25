from flask import redirect, render_template, request, send_from_directory, abort, jsonify, url_for, session
from flask_app import app
import os
import uuid
from flask_app.models.upload import File

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1]

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def file_upload():
    if "my_file" not in request.files:
        error_response = {
            "error": "File does not exist"
        }
        return jsonify(error_response)
    my_file = request.files["my_file"]
    extension = get_file_extension(my_file.filename)
    unique_filename = (uuid.uuid4().hex) + extension
    my_file.save(os.path.join(app.config["UPLOADED_DIR"], unique_filename))
    File.save({
        "file_name": unique_filename,
        "size": os.path.getsize(os.path.join(app.config["UPLOADED_DIR"], unique_filename)),
        "extension": extension,
        "users_id": session['user_id']
    })
    print(my_file)
    return {
        "success": "File has been successfully uploaded!"
    }