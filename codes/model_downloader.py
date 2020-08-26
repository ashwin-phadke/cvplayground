import tensorflow as tf
import urllib
import tarfile
import os
import wget


download_model_list = ["ssd_mobilenet_v2_coco_2018_03_29", "ssd_inception_v2_coco_2017_11_17",
 "faster_rcnn_inception_v2_coco_2018_01_28", "faster_rcnn_resnet50_coco",
 "faster_rcnn_nas", "faster_rcnn_resnet101_coco", "mask_rcnn_inception_v2_coco",
 "mask_rcnn_inception_resnet_v2_atrous_coco", "ssd_inception_v2_coco", "faster_rcnn_inception_v2_coco"]


# Download and extract model
def download_model(model_name):
    base_url = 'http://download.tensorflow.org/models/object_detection/'
    model_file = base_url + model_name +  '.tar.gz'
    print("Downloading {} model".format(model_name))
    path = os.getcwd()
    abc = os.path.join(os.path.dirname(path) , 'detect_models/' , model_name + '.tar.gz')
    #wget.download(model_file, os.path.join(os.path.dirname(path) , 'detect_models/' , model_name + '.tar.gz'))

    path_to_model_file = os.path.join(os.path.dirname(path) , 'detect_models/' , model_name + '.tar.gz')
    tar_file = tarfile.open(path_to_model_file)
    for file in tar_file.getmembers():
        file_name = os.path.basename(file.name)
        if 'frozen_inference_graph.pb' in file_name:
            tar_file.extract(file, model_file)


    return str(os.getcwd())



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


