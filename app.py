from flask import Flask, render_template, redirect, url_for, request
from models import Projects
import os
from database import session as db_session
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/projectimages'  # Folder for uploaded images
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensuring the folder for images exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    pobj = db_session.query(Projects).all()
    return render_template('index.html', pobj=pobj)

if __name__=="__main__":
    app.run(debug=True)
    
    

