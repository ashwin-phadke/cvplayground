# Computer Vision Playground

<p align="center">
  <img src="https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/logo.png" alt="Logo from pixabay images"/>
</p>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![fork](https://img.shields.io/github/forks/ashwin-phadke/cvplayground)](https://img.shields.io/github/forks/ashwin-phadke/cvplayground) [![fork](https://img.shields.io/badge/python-3.6%2B-orange)](https://img.shields.io/badge/python-3.6%2B-orange)

A computer vision playground to try and test end to end(test to deploy) computer vision pipeline. 

 **To contribute, create an issue and refer [Contributing](https://github.com/ashwin-phadke/cvplayground/blob/master/CONTRIBUTING.md) for possible options.**

App 1 : 

This app facilitates the user to just upload any desired video and check the detection accuracy based on the user selected Tensorflow model from model zoo without having to go through writing code for such commom task and can then make appropriate decision in the choice of the right model hence saving important development time.
- Screenshots :

![Landing Page of the app](https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/landing_page.png)
*This is the landing page when you start your Flask server. Image credits left- Tensorflow , right -Youtube,*
______________________________________________________________________________________

![Model Select Page](https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/model_select_page.png)
*Here you can choose a model to perform object detection on your desired video. All the models are from the Tensorflow model zoo and you can also add or remove models from this section to better suit your own deployed app. After selecting your model you then upload the video you would like to process using the select a file to upload option and click submit.*

_________________________________________________________________________________________

![List of models](https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/final_model_select.png)
*You can see what models are currently supported or available using the model select dropdown as shown*
_________________________________________________________________________________________

![Show user prompt](https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/model.png)
*Check to see whether you have selected a model and uploaded the file correctly before submitting the form to process your video.*
_________________________________________________________________________________________

![Processed Video page](https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/processed_download_page.png)
*You can now finally download the video processed with the Tensorflow model you seected earlier and see the results for yourself*

_________________________________________________________________________________________

  
- Name : Process videos for object detection using Tensorflow

- Models currently supported* : 

|                |DB Code                          |Model                         |
|----------------|-------------------------------|-----------------------------|
|1|ssdmv2i            |ssd_mobilenet_v2_coco           |
|2          |ssdiv2            |ssd_inception_v2_coco_2017_11_17    (Currently active)       |



- Database : SQLite

- UI based app version : https://cvplayground.herokuapp.com/

- Deployment ProcFile : added

- Languages, Tools, Frameworks : TensorFlow, Python, Flask, HTML+CSS+JS, SQLite database.

    ### Getting Started :

    - Check to see if the following structure exists else create the following directory structure : 
    ![Directory Structure](dir_struct.jpg?raw=true "Title")
    - The downloads folder will host all the processed files for sending the user to download and uploads for saving uploaded files.
    - The models folder is from the tensorflow models directory, you only need object detection folder from that.
    - codes has the main video object detection code.
    - db has the database sqlite file.
    - templates has the web HTML templates for user interaction.

    ### Installation :

    - Go inside the main project directory and execute  

        ``` pip install -r requirements.txt```

      command to install all the necessary requirements needed to run this project.

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
    - Open a terminal and execute 

        ``` python flask_server.py ```     

        or

        ```gunicorn -t 1000 flask_server:app```
        
        (compatible with Heroku too) to deploy on production using Gunicorn

      which will start the default flask_server at `localhost:5000` or whatever port you designate in the `flask_server.py` file.

    - You are now ready.

    ### Notes : 
    More model support coming soon. Status passing, pytest with code 5. Import requires tensorflow model folder inside codes directory, however if it is available in your path then ou can directly link to it. 
    More models can be downloaded and saved in detect_models, the model name needs to be added in the dictionary and saved accordingly in the database to take effect.
    Heroku slug size exceeding due to packages and the model.
    The slug size limits deploying this on Heroku , hence deploying to following services like AWS Beanstalk or Google app engine.

