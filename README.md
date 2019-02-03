# note-keeper
Manage personal notes in a multi-user environment, such as across an organisation.

Built using Flask in Python, website developed in HTML (template in CSS) and database managed in SQL. Based on online tutorial of Flask (http://flask.pocoo.org/docs/1.0/tutorial/), the code of which can be found at https://github.com/pallets/flask/tree/1.0.2/examples/tutorial - credits to the Pallets team for creating this easy-to-follow tutorial.

## 1. Getting Started - How to run the application
### Install the application
Download all the files in the repository. Use ```pip``` to install the application ```flaskr``` and all required packaages (recommended to open a new ```venv``` virtual environment) as ```.whl``` file.

First change into the required directory:
```
cd dist
```

Then install the ```.whl``` file.
```
pip install flaskr-1.0.0-py2.py3-none-any.whl
```

Then initialise the database for storing user data:
```
export FLASK_APP=flaskr
flask init-db
```

The database will be located at an instance folder with directory ```venv/var/flaskr-instance```.

## 2. How to use the API
### Running the application in development mode
First set application to ```flaskr``` and environment to development mode from main (```note-keeper```) directory:
```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

In development mode, this is hosted at http://127.0.0.1:5000/.

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


## 3. Built With - Choice of technology
- Flask in Python for the functionalities.
- HTTP for the website.
- CSS for the template of the app.
- SQL for the personal notes in a database.

Choice of the above technologies is mainly due to simplicity, since this is the first proper web application I have written. Also detailed guidance readily available online.

## 4. Other features in the future
Hope to:
- Implement note sharing feature across multiple users (read-only and edit modes).
- Support images.
- Sorting and filtering notes.
- Improve the look of the application.

## Acknowledgements
Credits to Thirdfort for the inspiration for this project, and the Pallets team for creating the Flask package and tutorial.

