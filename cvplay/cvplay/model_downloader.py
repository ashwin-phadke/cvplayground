# Do necessary imports
import os
import tarfile
import urllib
from urllib import request
from os import chdir
from pathlib import Path

import tensorflow as tf
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


# Download and extract model in the detect_models directory, to get the directory structure required for this project check README.
def download_model(model_name, pbtxt_name):
    base_url = 'http://download.tensorflow.org/models/object_detection/'
    model_file = base_url + model_name + '.tar.gz'
    print("Downloading {} model".format(model_name))
    path = Path('..')
    chdir(path)
    model_path = os.path.join(os.getcwd(), 'cvplay/', 'detect_models/')
    download_model_path = os.path.join(model_path, model_name + '.tar.gz')
    urllib.request.urlretrieve(url=model_file, filename=download_model_path)
    tar_file = tarfile.open(download_model_path)
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, os.path.join(model_path, model_name))
    os.remove(download_model_path)

    download_label_path = os.path.join(
        model_path, model_name, model_name, pbtxt_name)
    label_base_url = 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/'
    pbtxt_file = label_base_url + pbtxt_name
    urllib.request.urlretrieve(url=pbtxt_file, filename=download_label_path)
    print("Comleted Downloading model and config files")


if __name__ == "__main__":
    print("main")
