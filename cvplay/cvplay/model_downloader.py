# Do necessary imports
import os
import tarfile
import urllib
from os import chdir
from pathlib import Path

import tensorflow as tf
import wget

import logging

logger = logging.getLogger('model_downloader logging')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# List of model files to download, this list comprises of the most common models used. To add your model simply go
# to https://github.com/tensorflow/models/blob/archive/research/object_detection/g3doc/tf1_detection_zoo.md and select the name of your
# appropriate model to download

download_model_list = ["ssd_mobilenet_v2_coco_2018_03_29", "ssd_inception_v2_coco_2017_11_17",
                       "faster_rcnn_inception_v2_coco_2018_01_28", "faster_rcnn_resnet50_coco",
                       "faster_rcnn_nas", "faster_rcnn_resnet101_coco", "mask_rcnn_inception_v2_coco",
                       "mask_rcnn_inception_resnet_v2_atrous_coco", "ssd_inception_v2_coco", "faster_rcnn_inception_v2_coco"]


# Download and extract model in the detect_models directory, to get the directory structure required for this project check README.
def download_model(model_name):
    base_url = 'http://download.tensorflow.org/models/object_detection/'
    model_file = base_url + model_name + '.tar.gz'
    print("Downloading {} model".format(model_name))
    path = Path('..')
    chdir(path)
    model_path = os.path.join(os.getcwd(), 'detect_models/')
    download_model_path = os.path.join(model_path, model_name + '.tar.gz')
    wget.download(model_file, download_model_path)
    tar_file = tarfile.open(download_model_path)
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.path.join(model_path, model_name))

    return model_name


def start_model_download():
    for model_name in download_model_list:
        PATH_TO_MODEL_DIR = download_model(model_name)
        print("Downloaded {}", PATH_TO_MODEL_DIR)

# # Download labels file
# def download_labels(filename):
#     base_url = 'https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/'
#     label_dir = tf.keras.utils.get_file(fname=filename,
#                                         origin=base_url + filename,
#                                         untar=False)
#     label_dir = pathlib.Path(label_dir)
#     return str(label_dir)

# LABEL_FILENAME = 'mscoco_label_map.pbtxt'
# PATH_TO_LABELS = download_labels(LABEL_FILENAME)


if __name__ == "__main__":
    start_model_download()
