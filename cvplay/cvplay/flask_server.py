
import logging
import os
import sqlite3
import time
import uuid

#from webapp import app
from flask import (Flask, flash, redirect, render_template,
                   request, send_file)
from werkzeug.utils import secure_filename

from db_create import main as db
from flask_process import (process_pose_estimation, process_segment_image,
                           process_video, process_objdet_image, process_segment_video, process_image_pose_estimation)

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'static/'

app = Flask(__name__, static_folder=DOWNLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

app.secret_key = "secret key"

model_dict = {"ssdmv2i": ("ssd_mobilenet_v2_coco_2018_03_29", "ssd_mobilenet_v2_coco_2018_03_29.pbtxt"),
              "ssdiv2": ("ssd_inception_v2_coco_2017_11_17", "ssd_inception_v2_coco_2017_11_17.pbtxt"),
              "frcnnv2": ("faster_rcnn_inception_v2_coco_2018_01_28", "faster_rcnn_resnet50_coco_2018_01_28.pbtxt"),
              "frcnnr50": ("faster_rcnn_resnet50_coco_2018_01_28", "faster_rcnn_resnet50_coco_2018_01_28.pbtxt"),
              "mrcnniv2": ("mask_rcnn_inception_v2_coco_2018_01_28", "mask_rcnn_inception_v2_coco_2018_01_28")}

_MODEL_URLS = {
    'mobilenetv2_coco_voctrainaug':
        'deeplabv3_mnv2_pascal_train_aug_2018_01_29.tar.gz',
    'mobilenetv2_coco_voctrainval':
        'deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz',
    'xception_coco_voctrainaug':
        'deeplabv3_pascal_train_aug_2018_01_04.tar.gz',
    'xception_coco_voctrainval':
        'deeplabv3_pascal_trainval_2018_01_04.tar.gz',
}


def generate_uuid():
    """
    Generating Unique ID's for storing files in database, this is done in order to overcome file name issues and have a standard filename.
    """
    new_id = uuid.uuid4()
    logging.info('UUID created')
    return new_id


def check_db_exists():
    """
    Checks to see if the dataase file required for the app to function exists in the current directory and if not then creates it with all the required tables.
    """
    if not os.path.isfile('db/cvplayground.db'):
        print('Creating database, this might take a while')
        db()
        print('Database created. Starting the app now')
    else:
        print('Database already exists. Starting app now...')


def date_time():
    """
    Storing local timestamp for logging purposes.
    """
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S",)
    return time_string


def allowed_file(filename):
    """
    CHeck if file in allowed file.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower()


@app.route('/')
def upload_form():
    """
    Retunrs the homepage for the app located in templates folder.
    """
    return render_template('bootstrapindex.html')

# @app.route('/index', methods=['GET', 'POST'])
# def index():
# 	if request.method == 'POST':
# 		return url_for(upload_file)


@app.route('/upload_page', methods=['GET', 'POST'])
def show_form():
    """
    Returns Model selection page where choice of different models is given to the user.
    These models are from Tensorfloe model zoo from Tensorflow v1 and are downloaded as per request.
    """
    return render_template('modelselectindex.html')


@app.route('/upload_image_page', methods=['GET', 'POST'])
def show_image_form():
    """
    Returns Model selection page where choice of different models is given to the user.
    These models are from Tensorfloe model zoo
    from Tensorflow v1 and are downloaded as per request.
    """
    return render_template('modelselectimageobjdet.html')


@app.route('/segmentation_upload_page', methods=['GET', 'POST'])
def show_segmentation_form():
    """
    Returns the template to upload image and choose model
    to perform semantic segmentation using Deeplab v3.
    """
    return render_template('modelselectsegmentationindex.html')


@app.route('/video_segmentation_upload_page', methods=['GET', 'POST'])
def show_video_segmentation_form():
    """
    Returns the template to upload image and choose model to
    perform semantic segmentation using Deeplab v3.
    """
    return render_template('modelselectvideosegmentation.html')


@app.route('/pose_estimation_upload_page', methods=['GET', 'POST'])
def show_pose_estimation_form():
    """
    Returns the template to upload image and choose model to perform Pose Estimation.
    """
    return render_template('modelselectposeestimation.html')


@app.route('/image_pose_estimation_modelselect_page', methods=['GET', 'POST'])
def show_image_pose_estimation_form():
    """
    Returns the template to upload image and choose model to perform Pose Estimation.
    """
    return render_template('modelselectimageposeestimation.html')


@app.route('/upload_image_pose_estimation_page', methods=['POST', 'GET'])
def upload_image_pose_estimation_file():
    """
    Function to upload image for Pose Estimation and then send for processing.
    """

    # Check if the method was a POST request
    if request.method == 'POST':
        ip_address = request.remote_addr
        app.logger.info('User %s entered app ', ip_address)

        # Connect  to the database
        conn = sqlite3.connect('db/cvplayground.sqlite')
        logging.info('User %s entered app', ip_address)
        if 'file' not in request.files:
            if 'model' not in request.form:
                return redirect(request.url)

        # Get the uploaded file.
        file = request.files['file']

        # Get the name of the backbone network chosen by the user.
        backbone_model_name = request.form['radios']

        if file and allowed_file(file.filename):
            filename_save = secure_filename(file.filename)
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], filename_save)
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
            pbtxt_name = 'SegModel'
            cur.execute("INSERT INTO uploads (id, status, isUploaded, isProcessed, location, datetime, model_name, pbtxt_name) values(?, ?, ?, ?, ?, ?, ?, ?)",
                        (new_uuid, status, isUploaded, isProcessed, location, dtt, backbone_model_name, pbtxt_name))
            conn.commit()
            conn.close()
            logging.info('File saved successfully from %s user', ip_address)

            # Implement deeplab semantic segmentation over image through this call.
            img_path = process_image_pose_estimation()
            filename = new_uuid + '.png'
            time.sleep(5)

            # Return processed image
            return redirect('/downloadsegmentationfile/' + filename)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            logging.info('User %s did not save a video file', ip_address)
            return redirect(request.url)


@app.route('/upload_pose_estimation_page', methods=['POST', 'GET'])
def upload_pose_estimation_file():
    """
    Function to upload video for Pose Estimation and then send for processing.
    """

    # Check if the method was a POST request
    if request.method == 'POST':
        ip_address = request.remote_addr
        app.logger.info('User %s entered app ', ip_address)

        # Connect  to the database
        conn = sqlite3.connect('db/cvplayground.sqlite')
        logging.info('User %s entered app', ip_address)
        if 'file' not in request.files:
            if 'model' not in request.form:
                return redirect(request.url)

        # Get the uploaded file.
        file = request.files['file']

        # Get the name of the backbone network chosen by the user.
        backbone_model_name = request.form['radios']

        if file and allowed_file(file.filename):
            filename_save = secure_filename(file.filename)
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], filename_save)
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
            pbtxt_name = 'SegModel'
            cur.execute("INSERT INTO uploads (id, status, isUploaded, isProcessed, location, datetime, model_name, pbtxt_name) values(?, ?, ?, ?, ?, ?, ?, ?)",
                        (new_uuid, status, isUploaded, isProcessed, location, dtt, backbone_model_name, pbtxt_name))
            conn.commit()
            conn.close()
            logging.info('File saved successfully from %s user', ip_address)

            # Implement deeplab semantic segmentation over image through this call.
            img_path = process_pose_estimation()
            filename = img_path + '.mp4'
            time.sleep(5)

            # Return processed image
            return redirect('/downloadsegmentationfile/' + filename)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            logging.info('User %s did not save a video file', ip_address)
            return redirect(request.url)


@app.route('/upload_video_segmentation_page', methods=['POST', 'GET'])
def upload_video_segmentation_file():
    """
    Function to upload video for semantic segmentation over deeplab v3 and then send for processing.
    """

    # Check if the method was a POST request
    if request.method == 'POST':
        ip_address = request.remote_addr
        app.logger.info('User %s entered app ', ip_address)
        # Connect  to the database
        conn = sqlite3.connect('db/cvplayground.sqlite')
        logging.info('User %s entered app', ip_address)
        if 'file' not in request.files:
            if 'model' not in request.form:
                return redirect(request.url)

        # Get the uploaded file.
        file = request.files['file']

        # Get the name of the backbone network chosen by the user which is also a key from the _MODEL_URLS dictionary.
        backbone_model_name = request.form['radios']

        # Get the relevant pre trained model using the above key.
        download_model_name = _MODEL_URLS[backbone_model_name]

        if file and allowed_file(file.filename):
            filename_save = secure_filename(file.filename)
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], filename_save)
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
            pbtxt_name = 'SegModel'
            cur.execute("INSERT INTO uploads (id, status, isUploaded, isProcessed, location, datetime, model_name, pbtxt_name) values(?, ?, ?, ?, ?, ?, ?, ?)",
                        (new_uuid, status, isUploaded, isProcessed, location, dtt, download_model_name, pbtxt_name))
            conn.commit()
            conn.close()
            logging.info('File saved successfully from %s user', ip_address)

            # Implement deeplab semantic segmentation over image through this call.
            img_path = process_segment_video()
            filename = img_path + '.avi'
            time.sleep(5)

            # Return processed image
            return redirect('/downloadsegmentationfile/' + filename)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            logging.info('User %s did not save a video file', ip_address)
            return redirect(request.url)


@app.route('/upload_segmentation_page', methods=['POST', 'GET'])
def upload_segmentation_file():
    """
    Function to upload image for semantic segmentation over deeplab v3 and then send for processing.
    """

    # Check if the method was a POST request
    if request.method == 'POST':
        ip_address = request.remote_addr
        app.logger.info('User %s entered app ', ip_address)
        # Connect  to the database
        conn = sqlite3.connect('db/cvplayground.sqlite')
        logging.info('User %s entered app', ip_address)
        if 'file' not in request.files:
            if 'model' not in request.form:
                return redirect(request.url)

        # Get the uploaded file.
        file = request.files['file']

        # Get the name of the backbone network chosen by the user
        # which is also a key from the _MODEL_URLS dictionary.
        backbone_model_name = request.form['radios']

        # Get the relevant pre trained model using the above key.
        download_model_name = _MODEL_URLS[backbone_model_name]

        if file and allowed_file(file.filename):
            filename_save = secure_filename(file.filename)
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], filename_save)
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
            pbtxt_name = 'SegModel'
            cur.execute("INSERT INTO uploads (id, status, isUploaded, isProcessed, location, datetime, model_name, pbtxt_name) values(?, ?, ?, ?, ?, ?, ?, ?)",
                        (new_uuid, status, isUploaded, isProcessed, location, dtt, download_model_name, pbtxt_name))
            conn.commit()
            conn.close()
            logging.info('File saved successfully from %s user', ip_address)

            # Implement deeplab semantic segmentation over image through this call.
            img_path = process_segment_image()
            filename = img_path + '.png'
            time.sleep(5)

            # Return processed image
            return redirect('/downloadsegmentationfile/' + filename)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            logging.info('User %s did not save a video file', ip_address)
            return redirect(request.url)


@app.route('/uploads', methods=['POST', 'GET'])
def upload_file():
    """
    Upload Video file for object detection and then send for processing.
    """
    if request.method == 'POST':
        ip_address = request.remote_addr
        app.logger.info('User %s entered app ', ip_address)
        conn = sqlite3.connect('db/cvplayground.sqlite')
        logging.info('User %s entered app', ip_address)
    # check if the post request has the file part
        if 'file' not in request.files:
            if 'model' not in request.form:
                flash('No file part and no model selected.')
                return redirect(request.url)
        file = request.files['file']

        model = request.form['radios']
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


@app.route('/uploads_image', methods=['POST', 'GET'])
def upload_image_file():
    """
    Upload Image file for object detection and then send for processing.
    """
    if request.method == 'POST':
        ip_address = request.remote_addr
        app.logger.info('User %s entered app ', ip_address)
        conn = sqlite3.connect('db/cvplayground.sqlite')
        logging.info('User %s entered app', ip_address)
    # check if the post request has the file part
        if 'file' not in request.files:
            if 'model' not in request.form:
                flash('No file part and no model selected.')
                return redirect(request.url)
        file = request.files['file']

        model = request.form['radios']
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
            process_objdet_image()
            filename = new_uuid + '.png'
            time.sleep(5)
            return redirect('/downloadsegmentationfile/' + filename)

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            logging.info('User %s did not save a video file', ip_address)
            return redirect(request.url)


@app.route("/downloadsegmentationfile/<filename>", methods=['GET'])
def download_segfile(filename):
    """
    Download Image object detection, Video Segmentation,
    Image and Video Pose Estimation processed files.
    """
    return render_template('downloadsegmentindex.html', value=filename)


@app.route('/return-seg-files/<filename>')
def return_segfiles_tut(filename):
    """
    Returns the processed file to the download page for the user to view the file and download it.
    Image files are viewable currently whereas videos have download button.
    """
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True)


@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    """
    Download video obejct detection processed file.
    """
    return render_template('downloadindex.html', value=filename)


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    """
    Returns the processed file to the download page for the user to view the file and download it.
    Image files are viewable currently whereas videos have download button.
    """
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    check_db_exists()
    app.run(debug=True)
