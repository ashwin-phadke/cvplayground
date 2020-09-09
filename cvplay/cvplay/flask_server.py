import datetime
import logging
import os
import sqlite3
import subprocess
import time
import urllib.request
import uuid
from pathlib import Path

#from webapp import app
from flask import (Flask, flash, make_response, redirect, render_template,
                   request, send_file, send_from_directory, url_for)
from werkzeug.utils import secure_filename

#from flask_process import process_video
from cvplay.flask_process import process_video
from cvplay.db_create import main

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'static/'

app = Flask(__name__, static_folder=DOWNLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# logging.basicConfig(filename='cvplayground.log', level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


app.secret_key = "secret key"

# model_dict = {
#     "ssdmv2i": ("ssd_mobilenet_v2_coco", "mobilenet.pbtxt"),
#     "ssdiv2": ("ssd_inception_v2_coco_2017_11_17", "ssdinceptionv2.pbtxt"),
#     "frcnnv2": ("faster_rcnn_inception_v2_coco_2018_01_28", "frcnninceptionv2.pbtxt"),
#     "ssdmv2": ("faster_rcnn_resnet50_coco", "frcnnresnet50.pbtxt")
# }

model_dict = {"ssdmv2i": ("ssd_mobilenet_v2_coco_2018_03_29", "ssd_mobilenet_v2_coco_2018_03_29.pbtxt"),
                 "ssdiv2": ("ssd_inception_v2_coco_2017_11_17", "ssd_inception_v2_coco_2017_11_17.pbtxt"),
                 "frcnnv2": ("faster_rcnn_inception_v2_coco_2018_01_28", "faster_rcnn_resnet50_coco_2018_01_28.pbtxt"),
                 "ssdmv2": ("faster_rcnn_resnet50_coco", "faster_rcnn_resnet50_coco_2018_01_28.pbtxt")}

def generate_uuid():
    new_id = uuid.uuid4()
    logging.info('UUID created')
    return new_id


def date_time():
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S",)
    return time_string


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower()


@app.route('/')
def upload_form():
    return render_template('index.html')

# @app.route('/index', methods=['GET', 'POST'])
# def index():
# 	if request.method == 'POST':
# 		return url_for(upload_file)


@app.route('/upload_page', methods=['GET', 'POST'])
def show_form():
    return render_template('upload.html')


@app.route('/uploads', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        ip_address = request.remote_addr
        conn = sqlite3.connect('db/cvplayground.sqlite')
        logging.info('User %s entered app', ip_address)
    # check if the post request has the file part
        if 'file' not in request.files:
            if 'model' not in request.form:
                flash('No file part and no model selected.')
                return redirect(request.url)
        file = request.files['file']

        model = request.form['model']
        model_name, pbtxt_name = model_dict[model]

        if file.filename == '':
            flash('No file selected for uploading')
            logging.info("user %s did not select a file", ip_address)
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logging.info('User %s successfully saved file', ip_address)
            print("File saved successfully")
            cur = conn.cursor()
            new_uuid = str(generate_uuid())

            dtt = date_time()
            isUploaded = True
            isProcessed = False
            location = file_path
            status = 1
            cur.execute("INSERT INTO uploads (id, status, isUploaded, isProcessed, location, datetime, model_name, pbtxt_name) values(?, ?, ?, ?, ?, ?, ?, ?)",
                        (new_uuid, status, isUploaded, isProcessed, location, dtt, model_name, pbtxt_name))
            conn.commit()
            conn.close()
            logging.info('File saved successfully from %s user', ip_address)
            process_video()
            filename = new_uuid + '.mp4'
            time.sleep(5)
            return redirect('/downloadfile/' + filename)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            logging.info('User %s did not save a video file', ip_address)
            return redirect(request.url)


@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path,  as_attachment=True)


def package_main():
    app.run(debug=True)


if __name__ == "__main__":
    package_main()
    # app.run(debug=True)
