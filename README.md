# Cervantes
Cervantes is a web app made for the [Unbabel](https://unbabel.com/) Fullstack challenge. This small project uses the Unbabel Sandbox API to translate strings from one language to another.


## 💾 Stack
* Python 3.7.0
* Flask 1.0.2
* PostgreSQL 11
* Javascript (ES2015+)
* CSS (Bootstrap 4)
* HTML5


## 🛠️ Installation
### Python
Make sure you have the latest version of Python3 installed. If not, head over to the [download page](https://www.python.org/downloads/) and follow the instructions for your OS.


### Setting up the environment
Start by `clone`ing the repository into a directory of your choice:

```bash
git clone https://github.com/neivars/fullstack-coding-challenge.git cervantes
```

The above will create a `cervantes` directory in your current directory and copy the project source code into it.

With Python installed, it's wise to have a **Python environment** solution rolled up. I suggest [virtualenv](https://virtualenv.pypa.io/en/stable/), which you can install with `pip`.

```bash
pip install virtualenv
```

This will install the virtualenv package globally. Next, spin up a Python environment in the directory where you cloned the repository to.

```bash
cd cervantes
virtualenv venv
```

`venv` is now your local python environment, complete with a seperate Python interpreter and package directory. While this virtual environment is **active**, everything Python does will come from here first. Go ahead and activate venv.

**💻 Windows**
```bash
venv\Scripts\activate
```
**🍎🐧 Mac / \*nix**
```bash
source venv/bin/activate
```

You should now see a `(venv)` next to your terminal prompt. You're now isolated from your global Python installation.

If you want to deactivate the virtual environment.
```bash
deactivate
```


### Installing project dependencies
With your **virtual environment** active, go ahead and install the project's dependencies. They're listed in the `requirements.txt` at the root of the project, which we pass to `pip` through the `-r` option.

```bash
pip install -r requirements.txt
```

### Installing PostgresSQL and creating databases
This project makes use of the **PostgresSQL RDBMS**, and makes the assumption that **two databases exist** (one for _production_, and another for _testing_).

Go ahead and download [PostgresSQL](https://www.postgresql.org/) and follow the installation instructions for your OS.

Next, create two databases - one for use in _production_ and the other for use in _testing_, like **cervantes** and **cervantes_testing**.

Copy or rename `cervantes.example.yaml` into `cervantes.yaml`, open it and change the values of the `SQLALCHEMY_DATABASE_URI` keys in production and testing to the respective new databases, along with the host, port, user and password. Keep this file safe and secure, it now holds **secrets**.


### Setting a secret key
The web app needs a **secret key** to pass flashed session messages along back to the frontend. You can set it to any string you want, but a quick way to generate a random enough key is with Python itself.

```bash
python -c 'import os; print(os.urandom(16))'
```

Set the `SECRET_KEY` keys for both production and testing inside `cervantes.yaml`. You can have the production and testing `SECRET_KEY`s be different, if you wish.


### Set up development server
Flask can set up a development server at `127.0.0.1:5000` (by default). In order to spin up the server, Flask needs to know the project's entry point.

**💻 Windows**
```bash
set FLASK_APP=cervantes
```
**🍎🐧 Mac / \*nix**
```bash
export FLASK_APP=cervantes
```

If you want extra debug information, you can also (optionall) set the web app's environment.

**💻 Windows**
```bash
set FLASK_ENV=development
```
**🍎🐧 Mac / \*nix**
```bash
export FLASK_ENV=development
```

Finally, go ahead and run flask.

```bash
flask run
```

And visit http://127.0.0.1:5000.


## ✔️🔴 Testing
Cervantes is furnished with a testing suite ran by [`pytest`](https://docs.pytest.org/en/latest/). It has **100%** test coverage.

Run the test suite by calling pytest.

```bash
pytest
```
Run the test suite and collect coverage information by calling `coverage`.

```bash
coverage run -m pytest
```
The coverage can be reported by calling...

```bash
coverage report
```

... or ...

```bash
coverage html
```

... to generate a full HTML report in the `htmlcov` directory at the root of the project. Navigate inside and open `index.html` to see it in your browser.
