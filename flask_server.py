import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import urllib.request
from subprocess import Popen
#from webapp import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid
import sqlite3
import datetime
import time
import logging
from flask_process import process_video

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

logging.basicConfig(filename='cvplayground.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


app.secret_key = "secret key"

model_dict = {
	"ssdmv2i" : "ssd_mobilenet_v2_coco",
	"ssdiv2"  : "ssd_inception_v2_coco_2017_11_17",
	"frcnnv1" : "faster_rcnn_inception_v2_coco_2017_01_28",
	"ssdmv2"  : "faster_rcnn_resnet50_coco"
}


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

@app.route('/upload_page', methods=['GET','POST'])
def show_form():
	return render_template('upload.html')



@app.route('/uploads', methods=[ 'POST'])
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
		model_name = model_dict[model]

		if file.filename == '':
			flash('No file selected for uploading')
			logging.info("user %s did not select a file", ip_address)
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(file_path)
			logging.info('User %s successfully saved file', ip_address)
			# print(file_path)
			print("File saved successfully")
			cur = conn.cursor()
			new_uuid = str(generate_uuid())
			
			dtt = date_time()
			#print(dtt)
			isUploaded = True
			isProcessed = False
			location = file_path
			status = 1
			cur.execute("INSERT INTO uploads (id, status, isUploaded, isProcessed, location, datetime, model_name) values(?, ?, ?, ?, ?, ?, ?)",(new_uuid, status, isUploaded, isProcessed, location, dtt, model_name))
			conn.commit() 
			conn.close()
			logging.info('File saved successfully from %s user', ip_address)
			process_video()
			#objdetectionfunc(file_path)
			flash('File successfully uploaded')
			return redirect('/')
			
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			logging.info('User %s did not save a video file', ip_address)
			return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True)