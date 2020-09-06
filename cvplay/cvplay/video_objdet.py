# import the necessary packages
import argparse
import os
import sys
import tarfile
import time
import zipfile
from collections import defaultdict
from io import StringIO

import cv2
import imutils
import numpy as np
import six.moves.urllib as urllib
import tensorflow as tf
from imutils.video import FPS, VideoStream
from matplotlib import pyplot as plt
from PIL import Image

from cvplay.codes.models.research.object_detection.utils import label_map_util
from cvplay.codes.models.research.object_detection.utils import \
    visualization_utils as vis_util
from cvplay.model_downloader import start_model_download as smd
sys.path.append("..")


def objdetectionfunc(urlll, id, model_name, pbtxt_name):

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.8,
                    help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    VID_SAVE_PATH = 'static/'
    BASE_PATH = 'detect_models/'
    INFERENCE = 'frozen_inference_graph.pb'
    PATH_TO_CKPT = os.path.join(BASE_PATH, model_name + '/', INFERENCE)
    PATH_TO_PBTXT = os.path.join(BASE_PATH, model_name, pbtxt_name)

    if not os.path.exists(PATH_TO_CKPT) and os.path.exists(PATH_TO_PBTXT):
        smd()

    classes_90 = ["person", "bicycle", "car", "motorcycle",
                  "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
                  "unknown", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse",
                  "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "unknown", "backpack",
                  "umbrella", "unknown", "unknown", "handbag", "tie", "suitcase", "frisbee", "skis",
                  "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
                  "surfboard", "tennis racket", "bottle", "unknown", "wine glass", "cup", "fork", "knife",
                  "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
                  "pizza", "donut", "cake", "chair", "couch", "potted plant", "bed", "unknown", "dining table",
                  "unknown", "unknown", "toilet", "unknown", "tv", "laptop", "mouse", "remote", "keyboard",
                  "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "unknown",
                  "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

    CLASSES = classes_90  # New list of classess with 90 classess.
    print(CLASSES)

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    cvNet = cv2.dnn.readNetFromTensorflow(PATH_TO_CKPT, PATH_TO_PBTXT)

    # Change only if you have more than one webcams
    cap = cv2.VideoCapture(urlll)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(VID_SAVE_PATH + id + '.mp4',
                          fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        h = frame.shape[0]
        w = frame.shape[1]
        img = np.array(frame)
        cvNet.setInput(cv2.dnn.blobFromImage(
            img, size=(300, 300), swapRB=True, crop=False))
        detections = cvNet.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                print(idx)
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                             confidence * 100)
                cv2.rectangle(img, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(img, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

                print(label)

        out_img = cv2.resize(img, (640, 480))
        out.write(out_img)
        cv2.imshow('img', out_img)
    cap.release()
    out.release()
    cv2.destroyAllWindows()
