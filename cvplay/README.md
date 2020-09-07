# Computer Vision Playground

<p align="center">
  <img src="https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/logo.png" alt="Logo from pixabay images"/>
</p>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

A computer vision playground to try and test end to end(test to deploy) computer vision pipeline. 

 **To contribute, create an issue and refer [Contributing](https://github.com/ashwin-phadke/cvplayground/blob/master/CONTRIBUTING.md) for possible options.**


**Update** : A new and easy way to download models is now available in codes/model_downloader.py to easily download and extract multiple models from tensorflow model zoo.

App 1 : 

This app facilitates the user to just upload any desired video and check the detection accuracy based on the user selected Tensorflow model from model zoo without having to go through writing code for such commom task and can then make appropriate decision in the choice of the right model hence saving important development time.
- Screenshots :

![Landing Page of the app](https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/landing_page.png)
*This is the landing page when you start your Flask server. Image credits left- Tensorflow , right -Youtube,*
______________________________________________________________________________________

![Processed Video page](https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/processed_download_page.png)
*You can now finally download the video processed with the Tensorflow model you seected earlier and see the results for yourself*

_________________________________________________________________________________________

  
- Name : Process videos for object detection using Tensorflow

- Models currently supported* : 

|                |DB Code                          |Frozen graph name                         |Pbtxt file
|----------------|-------------------------------|-----------------------------|-----------------------------|
|1|ssdmv2i            |frozen_inference_graph.pb          |
|2          |ssdiv2            |ssd_inception_v2_coco_2017_11_17    (Currently active)       | ssdinceptionv2.pbtxt|


- Database : SQLite

- UI based app version : https://cvplayground.herokuapp.com/

- Deployment ProcFile : added

- Languages, Tools, Frameworks : TensorFlow, Python, Flask, HTML+CSS+JS, SQLite database.

    ### Getting Started :

    - Check to see if the following structure exists else create the following directory structure : 
    ![Directory Structure](dir_struct.jpg?raw=true "Title")

    - The downloads folder will host all the processed files for sending the user to download and uploads for saving uploaded files.

    - codes has the main video object detection code and model downloader with requirements for the tensorflow object detection api
    in the models sub directory.

    - db has the database sqlite file.

    - templates has the web HTML templates for user interaction.

    - detect_models hosts the model .pb and .pbtxt files for the desired model to use. Refer model_downloader.py to download the models in this directory.

    - Download the desired model and it's protoxt files from the link below and put them in detect_models folder.

    | Model Version  |  Version   |   Weights(.pb)   |   prototxt(.pbtxt)    |
    |----------|:-------------:|------:|-----:|
    |MobileNet-SSD v1 | 2017\_11\_17 | [weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2017_11_17.tar.gz) | [config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/ssd_mobilenet_v1_coco_2017_11_17.pbtxt) 
    |MobileNet-SSD v1 PPN |2018\_07\_03| [weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03.tar.gz) |[config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/ssd_mobilenet_v1_ppn_coco.pbtxt) 
    |MobileNet-SSD v2| 2018\_03\_29 |[weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz) |[config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/ssd_mobilenet_v2_coco_2018_03_29.pbtxt)|
    |Inception-SSD v2 |2017\_11\_17| [weights](http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2017_11_17.tar.gz) |[config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/ssd_inception_v2_coco_2017_11_17.pbtxt) |
    |MobileNet-SSD v3 (see [\#16760](https://github.com/opencv/opencv/pull/16760)) |2020\_01\_14 |[weights](http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v3_large_coco_2020_01_14.tar.gz) |[config](https://gist.github.com/dkurt/54a8e8b51beb3bd3f770b79e56927bd7) |
    |Faster-RCNN Inception v2| 2018\_01\_28 |[weights](http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz) |[config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/faster_rcnn_inception_v2_coco_2018_01_28.pbtxt) |
    |Faster-RCNN ResNet-50 |2018\_01\_28 |[weights](http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz)| [config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/faster_rcnn_resnet50_coco_2018_01_28.pbtxt)|
    |Mask-RCNN Inception v2| 2018\_01\_28| [weights](http://download.tensorflow.org/models/object_detection/mask_rcnn_inception_v2_coco_2018_01_28.tar.gz)| [config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt)|
    |EfficientDet-D0 |(see [\#17384](https://github.com/opencv/opencv/pull/17384))  | [weights](https://www.dropbox.com/s/9mqp99fd2tpuqn6/efficientdet-d0.pb?dl=1)| [config](https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/efficientdet-d0.pbtxt) |


    Furthermore, if you would like to convert your own models you can refer the following scripts for a better context to how to get the required files.
    * [tf\_text\_graph\_ssd.py](https://github.com/opencv/opencv/blob/master/samples/dnn/tf_text_graph_ssd.py)
    * [tf\_text\_graph\_common.py](https://github.com/opencv/opencv/blob/master/samples/dnn/tf_text_graph_common.py)
    * [tf\_text\_graph\_faster\_rcnn.py](https://github.com/opencv/opencv/blob/master/samples/dnn/tf_text_graph_faster_rcnn.py)
    * [tf\_text\_graph\_mask\_rcnn.py](https://github.com/opencv/opencv/blob/master/samples/dnn/tf_text_graph_mask_rcnn.py)

  ### Installation via Pip:
    - Almost all of your work is already done.
    - To use open your favorite code editor:

      ```
      import cvplay as cp
      cp.package_main()
      ```

    Your app is now running at `127.0.0.1:5000`

    ### Installation via zip:

    - Go inside the main project directory and execute  

        ``` pip install -r requirements.txt```

      command to install all the necessary requirements needed to run this project.

    - Use the `model_downloader.py file` . You can download all the models using this file to perform object detection with. 
    You can also select which models to download using the list at the very beginning of the script. 
    the script will automatically download models to the detect_models directory and unzip them as shown in the directory structure.

    - Create a `sqlite` database file inside `db` giving the name you wish. The project uses `cvplayground.sqlite` for simplicity.

    - Execute the below `create` statement to create the necessary tables inside the databse created.

    ```
    CREATE TABLE "uploads" (
	"id"	TEXT UNIQUE,
	"status"	NUMERIC,
	"isUploaded"	INTEGER,
	"isProcessed"	INTEGER,
	"location"	TEXT,
	"datetime"	TEXT,
	"model_name"	TEXT
     )

    ```

    OR simply go to `codes/db_create.py` and let it do all the work for you.
    - Open a terminal and execute 

        ``` python flask_server.py ```     

        or

        ```gunicorn -t 1000 flask_server:app```
        
        (compatible with Heroku too) to deploy on production using Gunicorn

      which will start the default flask_server at `localhost:5000` or whatever port you designate in the `flask_server.py` file.

    - You are now ready.

    ### Notes : 
    [UPDATE] :  With the change in how models are loaded you can now simply create a folder named as your model name with the model's `.pb` and `.pbtxt` and add it to the dictionary to make it work with your own model easily.

    
    More model support coming soon. Status passing, pytest with code 5. Import requires tensorflow model folder inside codes directory, however if it is available in your path then ou can directly link to it. 
    More models can be downloaded and saved in detect_models, the model name needs to be added in the dictionary and saved accordingly in the database to take effect.
    Heroku slug size exceeding due to packages and the model.
    The slug size limits deploying this on Heroku , hence deploying to following services like AWS Beanstalk or Google app engine.

