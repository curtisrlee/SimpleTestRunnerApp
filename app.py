import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import datetime as dt

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'abc'
db = MongoClient('localhost', 27017)['test_app']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        print(request.form)

        if 'name' not in request.form or not request.form['name']:
            flash('No name')

        if 'device' not in request.form or not request.form['device']:
            flash('No device')

        if 'file' not in request.files:
            flash('No file part')
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            # return redirect(request.url)
        
        if file and allowed_file(file.filename):
            timestamp = dt.datetime.utcnow()

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            entry = dict(request.form)
            entry['timestamp'] = timestamp
            entry['file'] = filename
            entry['status'] = "Queued"

            print(entry)

            db['queue'].insert_one(entry)

            # return redirect(url_for('download_file', name=filename))
        
    queue_items = enumerate(db['queue'].find({'status': 'Queued'}))
    completed_items = enumerate(db['queue'].find({'status': 'Completed'}))
        
    return render_template("index.html", queue=queue_items, completed=completed_items) 