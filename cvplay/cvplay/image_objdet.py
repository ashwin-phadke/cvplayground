# How to load a Tensorflow model using OpenCV
# Jean Vitor de Paulo Blog - https://jeanvitor.com/tensorflow-object-detecion-opencv/

# import the necessary packages
import argparse

import os
import sys
import cv2
import numpy as np
from model_downloader import download_model


sys.path.append("..")


def imageobjdetectionfunc(urlll, id, model_name, pbtxt_name):
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--confidence", type=float, default=0.8,
                    help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())
    # define save paths and path to models and it's pbtxt files
    IMAGE_SAVE_PATH = 'static/'
    BASE_PATH = 'detect_models/'
    INFERENCE = 'frozen_inference_graph.pb'

    PATH_TO_CKPT = os.path.join(
        BASE_PATH, model_name + '/', model_name, INFERENCE)
    if not os.path.exists(PATH_TO_CKPT):
        path_to_model, path_to_pbtxt = download_model(model_name, pbtxt_name)
    else:
        path_to_model = os.path.join(
            BASE_PATH, model_name + '/', model_name, INFERENCE)
        path_to_pbtxt = os.path.join(
            BASE_PATH, model_name + '/', model_name, pbtxt_name)
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
    print(CLASSES)
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    cvNet = cv2.dnn.readNetFromTensorflow(path_to_model, path_to_pbtxt)

    # Load a model imported from Tensorflow
    # tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')

    # Input image
    img = cv2.imread(urlll)
    (h, w) = img.shape[:2]

    # Use the given image as input, which needs to be blob(s).
    cvNet.setInput(cv2.dnn.blobFromImage(
        img, size=(300, 300), swapRB=True, crop=False))

    # Runs a forward pass to compute the net output
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

    # Show the image with a rectagle surrounding the detected objects
    cv2.imwrite(IMAGE_SAVE_PATH + id + '.png', img) 
    # cv2.imshow('Image', img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
