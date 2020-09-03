import argparse
import time

import cv2
import imutils
import numpy as np
from imutils.video import FPS, VideoStream

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#     help="path to image", default='index.jpg')
ap.add_argument("-c", "--confidence", type=float, default=0.8,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


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
# Leemos las clases disponibles en openImages
CLASSES = classes_90  # New list of classess with 90 classess.
print(CLASSES)

# Le damos colores a las cajas para cada clase
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Importamos el modelo de red
cvNet = cv2.dnn.readNetFromTensorflow('/home/aphadke/Github/cvplayground/detect_models/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb',
                                      '/home/aphadke/Github/cvplayground/detect_models/faster_rcnn_inception_v2_coco_2018_01_28/resnet.pbtxt')

# Leemos una imagen
# Change only if you have more than one webcams
cap = cv2.VideoCapture('/home/aphadke/Github/ODaaS/people.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    print('here')
    if not ret:
        print('this is why')
        break

    #img = cv2.imread(args["image"])

    # Obtenemos las dimensiones de la imagen
    h = frame.shape[0]  # Alto
    w = frame.shape[1]  # Ancho
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
    # out.write(out_img)
    cv2.imshow('img', out_img)
    # cv2.waitKey()
    if cv2.waitKey(25) & 0xFF == ord('q'):

        cv2.destroyAllWindows()
        # cap.release()
        # out.release()
