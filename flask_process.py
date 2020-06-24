import os
import os
from subprocess import Popen
from codes.video_objdet import objdetectionfunc
from pathlib import Path
import uuid
import sqlite3
from importlib import reload


def convert_ret_tuple(tup):
    str = ''.join(tup)
    return str


def process_video():

    conn = sqlite3.connect(
        'db/cvplayground.sqlite')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC")
    #cur.execute("SELECT id, location, model_name FROM uploads WHERE isProcessed=0 order by datetime DESC LIMIT 1")
    id, location, model_name = cur.fetchone()
    #print(id, location, model_name)
    if not (id, location):
        cur.execute(
            "SELECT id, location FROM uploads WHERE isProcessed=0 order by datetime DESC")
    objdetectionfunc(location, id, model_name)
    cur.execute("UPDATE uploads SET isProcessed=1  WHERE id='"+id+"'")
    conn.commit()
    conn.close()
    return id
    # reload(video_objdet)


if __name__ == "__main__":
    process_video()
