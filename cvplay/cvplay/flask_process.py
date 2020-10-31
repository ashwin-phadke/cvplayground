import sqlite3

from video_objdet import objdetectionfunc

from deeplab_sem_seg import preprocess
from run_video_pose_estimation import estimate_pose
from image_objdet import imageobjdetectionfunc


def convert_ret_tuple(tup):
    str = ''.join(tup)
    return str


def process_pose_estimation():
    conn = sqlite3.connect(
        'db/cvplayground.sqlite')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC")
    #cur.execute("SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC LIMIT 1")
    id, location, model_name = cur.fetchone()
    if not (id, location):
        cur.execute(
            "SELECT id, location FROM uploads WHERE isProcessed=0 order by datetime DESC")
    estimate_pose(id, location, model_name)
    cur.execute("UPDATE uploads SET isProcessed=1  WHERE id='"+id+"'")
    conn.commit()
    conn.close()
    return id


def process_segment_image():
    conn = sqlite3.connect(
        'db/cvplayground.sqlite')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC")
    #cur.execute("SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC LIMIT 1")
    id, location, model_name = cur.fetchone()
    if not (id, location):
        cur.execute(
            "SELECT id, location FROM uploads WHERE isProcessed=0 order by datetime DESC")
    preprocess(location, id, model_name)
    cur.execute("UPDATE uploads SET isProcessed=1  WHERE id='"+id+"'")
    conn.commit()
    conn.close()
    return id


def process_objdet_image():
    conn = sqlite3.connect(
        'db/cvplayground.sqlite')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, location, model_name, pbtxt_name FROM uploads WHERE isProcessed=0 order by datetime DESC")
    #cur.execute("SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC LIMIT 1")
    id, location, model_name, pbtxt_name = cur.fetchone()
    if not (id, location):
        cur.execute(
            "SELECT id, location FROM uploads WHERE isProcessed=0 order by datetime DESC")
    imageobjdetectionfunc(location, id, model_name, pbtxt_name)
    cur.execute("UPDATE uploads SET isProcessed=1  WHERE id='"+id+"'")
    conn.commit()
    conn.close()
    return id

def process_video():
    """
    Implements the call to proess videos for object detection.
    Function :
        objdetectionfunc()
    Arguments :
        location = file store location
        id : uuid of the file
        model name : chosen model name
        pbtxt_name : pbtxt file of the chosen model.
    """

    conn = sqlite3.connect(
        'db/cvplayground.sqlite')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, location, model_name, pbtxt_name FROM uploads WHERE isProcessed=0 order by datetime DESC")
    #cur.execute("SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC LIMIT 1")
    id, location, model_name, pbtxt_name = cur.fetchone()
    if not (id, location):
        cur.execute(
            "SELECT id, location FROM uploads WHERE isProcessed=0 order by datetime DESC")

    objdetectionfunc(location, id, model_name, pbtxt_name)
    cur.execute("UPDATE uploads SET isProcessed=1  WHERE id='"+id+"'")
    conn.commit()
    conn.close()
    return id


if __name__ == "__main__":
    process_video()
