# -*- coding: utf-8 -*-
"""DeepLab Demo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb

# Overview

This colab demonstrates the steps to use the DeepLab model to perform semantic segmentation on a sample input image. Expected outputs are semantic labels overlayed on the sample image.

### About DeepLab
The models used in this colab perform semantic segmentation. Semantic segmentation models focus on assigning semantic labels, such as sky, person, or car, to multiple objects and stuff in a single image.

## Import Libraries
"""

import logging
# Commented out IPython magic to ensure Python compatibility.
import os
import tarfile
import tempfile
import time

import cv2
import numpy as np
import tensorflow as tf
import tensorflow.compat.v1 as tf1
from matplotlib import gridspec
from matplotlib import pyplot as plt
from PIL import Image
from six.moves import urllib

"""## Import helper methods
These methods help us perform the following tasks:
* Load the latest version of the pretrained DeepLab model
* Load the colormap from the PASCAL VOC dataset
* Adds colors to various labels, such as "pink" for people, "green" for bicycle and more
* Visualize an image, and add an overlay of colors on various regions
"""


class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, tarball_path):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf1.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf1.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
          image: A PIL.Image object, raw input image.

        Returns:
          resized_image: RGB image resized from original input image.
          seg_map: Segmentation map of `resized_image`.
        """
        image = Image.open(image)
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(
            target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map

    def run_video(self, video_path, id):
        """Runs inference on a single video.

        Args:
        path: Path to video

        Returns:
        resized_image: RGB image resized from original input image.
        seg_map: Segmentation map of `resized_image`.
        """
        VID_SAVE_PATH = 'static/' + id + '.avi'

        cap = cv2.VideoCapture(video_path)
        wi = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        he = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        logging.info(wi, he)

        vwriter = cv2.VideoWriter(VID_SAVE_PATH,cv2.VideoWriter_fourcc(*'MJPG'),10, (wi, he))
        counter = 0
        fac = 2
        start = time.time()
        while True:
            ret, image = cap.read()
            
            if ret:
                counter += 1

                ## resize image

                height, width, channels = image.shape
                resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
                target_size = (int(resize_ratio * width), int(resize_ratio * height))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
                output = resized_image.copy()

                ## get segmentation map
                batch_seg_map = self.sess.run(
                self.OUTPUT_TENSOR_NAME,
                feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
                seg_map = batch_seg_map[0]

                ## visualize
                seg_image = label_to_color_image(seg_map).astype(np.uint8)

                ## overlay on image
                alpha = 0.7
                cv2.addWeighted(seg_image, alpha, output, 1 - alpha, 0, output)

                output = cv2.resize(output, (wi, he), interpolation=cv2.INTER_AREA)
    #             outimg = 'image_' + str(counter) + '.jpg'
    #             cv2.imwrite(os.path.join(os.getcwd(), 'test_out', outimg),output)
                vwriter.write(output)
            else:
                break
                
        end = time.time()
        logging.info("Frames and Time Taken: ", counter, end-start)
        cap.release()
        vwriter.release()
        return VID_SAVE_PATH


def create_pascal_label_colormap():
    """Creates a label colormap used in PASCAL VOC segmentation benchmark.

    Returns:
      A Colormap for visualizing segmentation results.
    """
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)

    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
        ind >>= 3

    return colormap


def label_to_color_image(label):
    """Adds color defined by the dataset colormap to the label.

    Args:
      label: A 2D array with integer type, storing the segmentation label.

    Returns:
      result: A 2D array with floating type. The element of the array
        is the color indexed by the corresponding element in the input label
        to the PASCAL color map.

    Raises:
      ValueError: If label is not of rank 2 or its value is larger than color
        map maximum entry.
    """
    if label.ndim != 2:
        raise ValueError('Expect 2-D input label')

    colormap = create_pascal_label_colormap()

    if np.max(label) >= len(colormap):
        raise ValueError('label value too large.')

    return colormap[label]


def vis_segmentation(image, seg_map, MODEL, FULL_COLOR_MAP, FULL_LABEL_MAP, LABEL_NAMES, id):
    """Visualizes input image, segmentation map and overlay view."""
    IMG_SAVE_PATH = 'static/' + id + '.png'
    plt.figure(figsize=(15, 5))
    grid_spec = gridspec.GridSpec(1, 4, width_ratios=[6, 6, 6, 1])

    plt.subplot(grid_spec[0])
    plt.imshow(image)
    plt.axis('off')
    plt.title('input image')

    plt.subplot(grid_spec[1])
    seg_image = label_to_color_image(seg_map).astype(np.uint8)
    plt.imshow(seg_image)
    plt.axis('off')
    plt.title('segmentation map')

    plt.subplot(grid_spec[2])
    plt.imshow(image)
    plt.imshow(seg_image, alpha=0.7)
    plt.axis('off')
    plt.title('segmentation overlay')

    unique_labels = np.unique(seg_map)
    ax = plt.subplot(grid_spec[3])
    plt.imshow(
        FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
    ax.yaxis.tick_right()
    plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
    plt.xticks([], [])
    ax.tick_params(width=0.0)
    plt.grid('off')
    plt.savefig(IMG_SAVE_PATH)
    return IMG_SAVE_PATH


def preprocess(location, id, model_name):

    LABEL_NAMES = np.asarray([
        'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
        'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
        'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
    ])

    FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
    FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)

    """## Select a pretrained model
    We have trained the DeepLab model using various backbone networks. Select one from the MODEL_NAME list.
    """

    # @param ['mobilenetv2_coco_voctrainaug', 'mobilenetv2_coco_voctrainval', 'xception_coco_voctrainaug', 'xception_coco_voctrainval']
    # MODEL_NAME = 'mobilenetv2_coco_voctrainaug'

    _DOWNLOAD_URL_PREFIX = 'http://download.tensorflow.org/models/'
    _TARBALL_NAME = 'deeplab_model.tar.gz'

    model_dir = tempfile.mkdtemp()
    tf.io.gfile.makedirs(model_dir)

    download_path = os.path.join(model_dir, _TARBALL_NAME)
    logging.info('downloading model, this might take a while...')
    urllib.request.urlretrieve(_DOWNLOAD_URL_PREFIX + model_name,
                               download_path)
    logging.info('download completed! loading DeepLab model...')

    MODEL = DeepLabModel(download_path)
    logging.info('model loaded successfully!')

    """## Run on sample images

    Select one of sample images (leave `IMAGE_URL` empty) or feed any internet image
    url for inference.

    Note that this colab uses single scale inference for fast computation,
    so the results may slightly differ from the visualizations in the
    [README](https://github.com/tensorflow/models/blob/master/research/deeplab/README.md) file,
    which uses multi-scale and left-right flipped inputs.
    """

    # SAMPLE_IMAGE = 'image1'  # @param ['image1', 'image2', 'image3']
    # IMAGE_URL = ''  # @param {type:"string"}

    # _SAMPLE_URL = ('https://github.com/tensorflow/models/blob/master/research/'
    #                'deeplab/g3doc/img/%s.jpg?raw=true')

    image_url = location
    filename, file_extension = os.path.splitext(image_url)
    extensions_list = ['.mp4', '.avi', '.mov', '.mkv']
    if file_extension in extensions_list:
        vid_path = MODEL.run_video(image_url, id)
        return vid_path
    else:
        #image_url = IMAGE_URL or _SAMPLE_URL % SAMPLE_IMAGE
        img_path = run_visualization(image_url, MODEL, FULL_COLOR_MAP,
                                    FULL_LABEL_MAP, LABEL_NAMES, id)
        return img_path


def run_visualization(url, MODEL, FULL_COLOR_MAP, FULL_LABEL_MAP, LABEL_NAMES, id):
    """Inferences DeepLab model and visualizes result."""
    # try:
    #     f = urllib.request.urlopen(url)
    #     jpeg_str = f.read()
    #     original_im = Image.open(BytesIO(jpeg_str))
    # except IOError:
    #     logging.info('Cannot retrieve image. Please check url: ' + url)
    #     return

    logging.info('running deeplab on image %s...' % url)
    resized_im, seg_map = MODEL.run(url)

    img_path = vis_segmentation(resized_im, seg_map, MODEL,
                                FULL_COLOR_MAP, FULL_LABEL_MAP, LABEL_NAMES, id)
    return img_path


if __name__ == "__main__":
    try:
        preprocess()
    except Exception as e:
        logging.info(e)

"""## What's next

* Learn about [Cloud TPUs](https://cloud.google.com/tpu/docs) that Google designed and optimized specifically to speed up and scale up ML workloads for training and inference and to enable ML engineers and researchers to iterate more quickly.
* Explore the range of [Cloud TPU tutorials and Colabs](https://cloud.google.com/tpu/docs/tutorials) to find other examples that can be used when implementing your ML project.
* For more information on running the DeepLab model on Cloud TPUs, see the [DeepLab tutorial](https://cloud.google.com/tpu/docs/tutorials/deeplab).
"""
