import argparse
import logging
import time

import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-Video')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0


def estimate_pose(id, video, model):
    """
    Estimate pose using input video.
    """

    VID_SAVE_PATH = 'static/'
    BASE_PATH = 'models/'
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(VID_SAVE_PATH + id + '.mp4',
                          fourcc, 20.0, (640, 480))

    parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    parser.add_argument('--showBG', type=bool, default=True,
                        help='False to show skeleton only.')
    args = parser.parse_args()

    # logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))

    # Default resolution 432x368, to use this simply replace target with w,h where :
    # w, h = model_wh(args.resolution)

    e = TfPoseEstimator(get_graph_path(model), target_size=(300, 300))
    cap = cv2.VideoCapture(video)

    if cap.isOpened() is False:
        logging.error("Error opening video stream or file")
    while cap.isOpened():
        ret_val, image = cap.read()
        if not ret_val:
            break

        humans = e.inference(image)
        if not args.showBG:
            image = np.zeros(image.shape)
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        fps_time = time.time()
        cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        resized = cv2.resize(image, (640, 480))
        out.write(resized)
        cv2.imshow('tf-pose-estimation result', resized)

        if cv2.waitKey(1) == 27:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    e.persistent_sess.close()


logger.debug('finished+')
