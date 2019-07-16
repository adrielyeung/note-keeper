# note-keeper
Manage personal notes in a multi-user environment, such as across an organisation.

Built using Flask 1.0 in Python 3, website developed in HTML (template in CSS) and database managed in SQLite 3. The scripts and this guide are based on online tutorial of Flask (http://flask.pocoo.org/docs/1.0/tutorial/), the code of which can be found at https://github.com/pallets/flask/tree/1.0.2/examples/tutorial - credits to the Pallets team for creating this easy-to-follow tutorial.

## 1. Getting Started - How to run the application
### Install the application
Download all the files in the repository. Use ```pip``` to install the application ```flaskr``` and all required packaages (recommended to open a new ```venv``` virtual environment) as ```.whl``` file.

First initialise ```venv``` then activate:
```
python -m venv venv
venv\Scripts\activate
```

Ensure that package Wheel is installed in order to install the ```.whl``` file:
```
pip install wheel
```

Then install the ```.whl``` file and its dependencies:
```
pip install dist\flaskr-1.0.0-py2.py3-none-any.whl
```

Then initialise the database for storing user data:

(Windows)
```
set FLASK_APP=flaskr
flask init-db
```

(Linux and Mac)
```
export FLASK_APP=flaskr
flask init-db
```

The database will be located at the ```instance``` folder.

## 2. How to use the API
### Running the application in development mode
First set application to ```flaskr``` and environment to development mode from main (```note-keeper```) directory:

(Windows) (For Linux and Mac, use ```export``` instead of ```set```.)
```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

In development mode, this is hosted at http://127.0.0.1:5000/. Use keyboard ```CTRL-C``` to stop serving.

### Scripts
#### App
The functionalities are provided by the scripts in the ```flaskr``` folder (See docstring within each function to discover their uses):

- ```flaskr\__init___.py``` provides the initialisation function for the app.
- ```flaskr\auth.py``` provides authenication (logging in and out) functions.
- ```flaskr\db.py``` provides the database interaction functions (both for storing user data and each user's notes).
- ```flaskr\note.py``` provides the functions for creating, updating, deleting and archiving/unarchiving notes.
- ```flaskr\schema.sql``` sets up the two tables (one for storing user data and one for each user's notes).

The ```flaskr\templates``` folder contains HTML templates for each page:

- ```templates\base.html``` is the base layout with the login/register links.
- ```templates\auth``` contains scripts for login and register pages.
- ```templates\note``` contains scripts for main (index), archive, creating and updating pages.

```flaskr\static\style.css``` sets the style of the webpages.

#### Test
The test scripts in the ```tests``` folder corresponds to each script in the ```flaskr``` folder (```test_factory.py``` tests the ```__init__.py``` script).
- ```conftest.py``` provides a fake user and app (in terms of Python fixtures) for testing.
- ```data.sql``` stores the data of a fake user and a fake note for testing.

### Running the tests
We will need packages ```pytest``` and ```coverage``` to perform the tests and calculate the percentage of code tested respectively:
```
pip install pytest coverage
```

The tests are located in the ```tests``` directory. To run them, simply use the ```pytest``` command from the main directory (```note-keeper```). To request a coverage report, use ```coverage``` command to run ```pytest```:
```
coverage run -m pytest
```

To generate a HTML report (an example one is attached in the ```tests``` directory):
```
coverage html
```
which generates the report (```index.html```) to the ```htmlcov``` directory.

### Deployment
Generate a random secret key for extra security by running Python in the terminal:
```
import os
print(os.urandom(16))
```
Then copy the output into the ```SECRET_KEY='dev'``` line, replacing ```'dev'```.

Use a production server instead of the development server in ```flask run```, for example Waitress (https://docs.pylonsproject.org/projects/waitress/en/stable/):
```
pip install waitress
python
```
In the Python console:
```
import waitress
import flaskr
waitress.serve(flaskr.create_app())
```
Then go to the URL as provided. Use keyboard ```CTRL-C``` to stop serving.

## 3. Built With - Choice of technology
- Flask 1.0 in Python 3 for the functionalities.
- HTTP for the website.
- CSS for the template of the app.
- SQLite 3 for the personal notes in a database.

Choice of the above technologies is mainly due to simplicity, since this is the first proper web application I have written. Also detailed guidance readily available online.

## 4. Other features in the future
Hope to:
- Implement note sharing feature across multiple users (read-only and edit modes).
- Support images.
- Sorting and filtering notes.
- Improve the look of the application.

## Acknowledgements
Credits to Thirdfort for the inspiration for this project, and the Pallets team for creating the Flask package and tutorial.

