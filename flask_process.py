import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
from subprocess import Popen
#from webapp import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from codes import video_objdet
#from codes.video_objdet import objdetectionfunc
from codes.temp_vid_objdet import dectect_func
from pathlib import Path
import uuid
import sqlite3

# UPLOAD_FOLDER = '/tensorflow/uploads'

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "secret key"


def convert_ret_tuple(tup):
    str = ''.join(tup)
    return str

@app.route('/')
def process_video():
    # isf = True
    # while isf:
    conn = sqlite3.connect(
        'db/cvplayground.sqlite')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC")
    #cur.execute("SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC LIMIT 1")
    id, location, model_name = cur.fetchone()
    print(id, location, model_name)
    if not (id, location):
        cur.execute(
        "SELECT id, location FROM uploads WHERE isProcessed=0 order by datetime DESC")
    #objdetectionfunc(location, id, model_name)s
    dectect_func(location, id, model_name)
    cur.execute("UPDATE uploads SET isProcessed=1  WHERE id='"+id+"'")
    conn.commit()
    conn.close()
    print('yes')


# if __name__ == "__main__":
#     process_video()
    # try :
    #     #app.run(port=5555, debug=True)
    #     process_video()
    # except Exception as e:
    #     print(e)
        
    # 


    # process_video()
