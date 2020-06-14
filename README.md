# Computer Vision Playground
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
A computer vision playground to try and test end to end(test to deploy) computer vision pipeline. 


App 1 : 

- Name : Process videos for object detection using Tensorflow

- Models currently supported* : 

|                |DB Code                          |Model                         |
|----------------|-------------------------------|-----------------------------|
|1|ssdmv2i            |ssd_mobilenet_v2_coco           |
|2          |ssdiv2            |ssd_inception_v2_coco_2017_11_17           |


due to heroku space limitations.

More model support coming soon. Status passing, pytest with code 5. Import requires tensorflow model folder inside codes directory, however if it is available in your path then ou can directly link to it. 
Heroku slug size exceeding due to packages and the model.

- Database : SQLite

- Current app version : https://cvplayground.herokuapp.com/

- Deployment ProcFile : added

- Languages, Tools, Frameworks : TensorFlow, Python, Flask, HTML+CSS+JS, SQLite database.

    ### Getting Started

    - Check to see if the following structure exists else create the following directory structure : 
    ![Directory Structure](dir_struct.jpg?raw=true "Title")
    - The downloads folder will host all the processed files for sending the user to download and uploads for saving uploaded files.
    - The models folder is from the tensorflow models directory, you only need object detection folder from that.
    - codes has the main video object detection code.
    - db has the database sqlite file.
    - templates has the web HTML templates for user interaction.

    ### Installation 

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

      which will start the default flask_server at `localhost:5000` or whatever port you designate in the `flask_server.py` file.

    - You are now ready.

