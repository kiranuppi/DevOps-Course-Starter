# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to create a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

We are using Trello to interact with our To-Do App and hence you need to create an developer account in Trollo and have the API_KEY, API_VALUE and Board Id inorder to interact with Trello APIs

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

## Running the App in a VM
 run vagrant up
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App in a Docker container

### Running in Development mode : 
First build the Docker Image :  
```bash
docker build --target development --tag todo-app:dev . 
```
Then Run, 
```bash
docker run --env-file ./.env  -p  5000:8080 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app. 

### Running in Production mode using gunicorn : 
First build the Docker Image :  
```bash
docker build --target production --tag todo-app:prod . 
```
Then Run, 
```bash
docker run --env-file ./.env -p 5100:8080 todo-app:prod     
```
Now visit [`http://localhost:5000/`](http://localhost:5100/) in your web browser to view the app.

## Running the App in a Docker container using Docker compose
```bash
docker-compose up --build 
```

Now visit [`http://localhost:8080/`](http://localhost:8080/) in your web browser to view the app.