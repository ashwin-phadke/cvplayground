# Computer Vision Playground

<p align="center">
  <img src="https://raw.githubusercontent.com/ashwin-phadke/cvplayground/master/readme_assets/logo.png" alt="Logo from pixabay images"/>
</p>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) 
[![fork](https://img.shields.io/github/forks/ashwin-phadke/cvplayground)](https://img.shields.io/github/forks/ashwin-phadke/cvplayground)
[![fork](https://img.shields.io/badge/python-3.6%2B-orange)](https://img.shields.io/badge/python-3.6%2B-orange)
[![stars](https://img.shields.io/github/stars/ashwin-phadke/cvplayground)](https://img.shields.io/github/stars/ashwin-phadke/cvplayground)
[![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

A computer vision playground to try and test end to end(test to deploy) computer vision pipeline. 

 **To contribute, create an issue and refer [Contributing](https://github.com/ashwin-phadke/cvplayground/blob/master/CONTRIBUTING.md) for possible options.**


- Currently Live apps :
   - TensorFlow Object Detection
   - Semantic Segmentation DeepLab

- Database : 
  - SQLite

- Languages, Tools, Frameworks : 
  - TensorFlow, Python, Flask, HTML+CSS+JS, SQLite database.

### Installation via Pip:
- Almost all of your work is already done.
- To use open your favorite code editor:

  ```
  import cvplay as cp
  cp.package_main()
  ```

- Your app is now running at `127.0.0.1:5000`

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
"model_name"	TEXT,
"pbtxt_name"  TEXT
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


More model support coming soon. Status passing, pytest with code 5. Import requires tensorflow model folder inside codes directory, however if it is available in your path then you can directly link to it. 
More models can be downloaded and saved in detect_models, the model name needs to be added in the dictionary and saved accordingly in the database to take effect.
Heroku slug size exceeding due to packages and the model.
The slug size limits deploying this on Heroku , hence deploying to following services like AWS Beanstalk or Google app engine.

