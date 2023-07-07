import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from threading import Thread
from waitress import serve
import csv
import json
import sensai


UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'

ALLOWED_EXTENSIONS = {'csv', 'txt'}

app = Flask(__name__)
status = None
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('processing', name=filename))
    return render_template('upload.html')

def check_file(filename: str):
    global status
    status = 0
    current = 0
    input_file = open(f"./uploads/{filename}", "r", newline='', errors="ignore")
    output_file = open(f"./output/{filename}", "w")
    data = input_file.readlines()
    total = len(data)
    writer = csv.writer(output_file)
    for line in data:
        if line == "" or line == "\n":
            pass
        else:
            print("done one")
            score = sensai.sentiment_analysis(line)
            data = [line[:-2], score[0]["label"]]
            writer.writerow(data)
            current += 1
            status =int((current/total) * 100)

@app.route('/processing/<name>')
def processing(name):
    print("made it here?")
    print(name)
    t1 = Thread(target=check_file, args=(name,))
    t1.start()
    print("started thread and continued on!")
    return render_template("processing.html", name=name)

@app.route('/status', methods=['GET'])
def getStatus():
    statusList={'status': status}
    return json.dumps(statusList)

@app.route('/output/<name>')
def download_file(name):
    return send_from_directory(OUTPUT_FOLDER, name)
# @app.route('/uploads/<name>')
# def download_file(name):

@app.route('/stats/<name>')
def stats(name):
    input_file = open (f"./output/{name}", "r")
    data = input_file.readlines()
    total = 0
    positive = 0
    negative = 0
    for line in data:
        if line[-9:] == "POSITIVE\n":
            positive += 1
            total += 1 
        elif line[-9:] == "NEGATIVE\n":
            negative += 1
            total += 1
    input_file.close()
    return render_template("stats.html", name=name, positive=int((positive/total) * 100), negative=int((negative/total) * 100))

serve(app, host="0.0.0.0", port=8080)
print("this is runnign")