from flask import Flask
import os

app = Flask(__name__)

app.secret_key = "babaBoomBoxX78$"

app.config['UPLOADED_DIR'] = os.path.join(app.instance_path, "uploads")

if not os.path.exists(app.config['UPLOADED_DIR']):
    os.makedirs(app.config['UPLOADED_DIR'])