# import the necessary packages
import argparse
import logging
import os
import sys

import cv2
import numpy as np

from model_downloader import download_model

sys.path.append("..")


# Object detection function

def objdetectionfunc(urlll, id, model_name, pbtxt_name):
    """
    Implements the function to proess videos for object detection.
    Function :
        objdetectionfunc()
    Arguments :
        location = file store location
        id : uuid of the file
        model name : chosen model name
        pbtxt_name : pbtxt file of the chosen model.
        Confidence : minimum probability to filter weak detections
    """

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.8,
                    help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    # define save paths and path to models and it's pbtxt files
    VID_SAVE_PATH = 'static/'
    BASE_PATH = 'detect_models/'
    INFERENCE = 'frozen_inference_graph.pb'

    PATH_TO_CKPT = os.path.join(
        BASE_PATH, model_name + '/', model_name, INFERENCE)
    if not os.path.exists(PATH_TO_CKPT):
        path_to_model, path_to_pbtxt = download_model(model_name, pbtxt_name)
    else :
        path_to_model = os.path.join(BASE_PATH, model_name + '/', model_name, INFERENCE)
        path_to_pbtxt = os.path.join(BASE_PATH, model_name + '/', model_name, pbtxt_name)
    # Define the COCO classes set.
    classes_90 = ["background", "person", "bicycle", "car", "motorcycle",
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
    logging.info(CLASSES)
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    cvNet = cv2.dnn.readNetFromTensorflow(path_to_model, path_to_pbtxt)

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
                logging.info(idx)
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

                logging.info(label)

        out_img = cv2.resize(img, (640, 480))
        out.write(out_img)
        cv2.imshow('img', out_img)
    cap.release()
    out.release()
    cv2.destroyAllWindows()
