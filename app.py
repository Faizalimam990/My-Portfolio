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

@app.route("/upload_project_items/", methods=['GET', 'POST'])
def upload_project():
    if request.method == 'POST':
        title = request.form['Title']
        description = request.form['Description']
        category = request.form['Category']
        project_link = request.form['project_link']
        image = request.files['image']

        # Handle file upload
        if image and allowed_file(image.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(filename)

            # Create new project entry
            new_project = Projects(
                Title=title,
                Description=description,
                Category=category,
                project_link=project_link,
                image_filename=image.filename
            )
            db_session.add(new_project)
            db_session.commit()
            return redirect(url_for('index'))  # Use 'index' as the redirect URL

    return render_template('upload_project.html')

@app.route("/project_detail/<int:id>")
def project_detail(id):
    # Query the database to get the project details based on the projectid
    project = db_session.query(Projects).filter_by(id=id).first()
    return render_template('project_detail.html', project=project)

@app.route("/admin/projects")
def all_project():
    all_pro=db_session.query(Projects).all()

    return render_template("allproject.html",all_pro=all_pro)
@app.route("/admin/deleteproject/<int:id>/")
def deleteproject(id):
    projectid=db_session.query(Projects).filter_by(id=id).first()
    db_session.delete(projectid)
    return redirect(url_for('all_project'))


if __name__=="__main__":
    app.run(debug=True)
    
    

