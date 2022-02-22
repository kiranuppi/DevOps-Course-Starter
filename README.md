# DevOps Apprenticeship: Project Exercise

## Links
* Travis Build : [`https://app.travis-ci.com/github/kiranuppi/DevOps-Course-Starter`](https://app.travis-ci.com/github/kiranuppi/DevOps-Course-Starter)
* Source Code : [`https://github.com/kiranuppi/DevOps-Course-Starter`](https://github.com/kiranuppi/DevOps-Course-Starter)
* Application URL : [`https://production-ku-todo-app.azurewebsites.net/home`](https://production-ku-todo-app.azurewebsites.net/home)
* Azure Resources : [`https://portal.azure.com/#@softwireacademy.onmicrosoft.com/resource/subscriptions/d33b95c7-af3c-4247-9661-aa96d47fccc0/resourceGroups/OpenCohort1_KiranUppinkudru_ProjectExercise/overview`](https://portal.azure.com/#@softwireacademy.onmicrosoft.com/resource/subscriptions/d33b95c7-af3c-4247-9661-aa96d47fccc0/resourceGroups/OpenCohort1_KiranUppinkudru_ProjectExercise/overview)

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


## Tests

### Unit and Integration Tests
You can run both unit and integration tests suites using pytest. Run this from the root directory:

`$ poetry run pytest tests`

### End to End Tests
You can run End to End tests suites using pytest. Check following dependencies are met:
* Firefox is installed on your system
* [`geckodriver`](https://github.com/mozilla/geckodriver/releases) is available ideally in the system/path or at least in the project folder.

Run this from the root directory:

    `$ poetry run pytest tests/tests_e2e`


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
docker run --env-file ./.env  -p  5000:8080 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app- todo-app:dev
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
Now visit [`http://localhost:5100/`](http://localhost:5100/) in your web browser to view the app.

## Running the App in a Docker container using Docker compose
```bash
docker-compose up --build 
```

Now visit [`http://localhost:8080/`](http://localhost:8080/) in your web browser to view the app.

## Running the tests in a Docker container 
Running Unit and Integration tests can be run with below command

```bash
docker run --env-file ./.env.test todo-app:test tests
```

Running End to End tests can be run with below command

```bash
docker run --env-file ./.env.test todo-app:test tests_e2e
```

## Travis CI
#### Set up Travis CI for your repository
Travis CI is set up to work well with GitHub but for it to work you need to enable it for any repository you want to use it for.

* Go to [`Travis-ci.com`](Travis-ci.com) and Sign in with GitHub credentials.
* Accept the Authorization of Travis CI. You’ll be redirected to GitHub.
* Click on your profile picture in the top right of your Travis Dashboard, click Settings and then the green Activate button, and select the project repository to use with Travis CI
* We now want to add a .travis.yml file which defines how to perform docker build and execute tests on Travis server.
* When we push .travis.yml to the repository, Travis server will pick this up and starts executing the instructions that are defined in the .travis.yml file.

## Heroku Deployment - Continuous Deployment
#### Step 1: Create & Configure Heroku App

First, create a new Heroku app either using the web interface or CLI. You should already have a Heroku account from this Module's workshop. If not, set one up now - it's free. Make a note of the app's name.
Once you've created an app, you'll need to provide it with the production environment variables your code needs to run. That will include your trello API credentials, and the board ID you want to use.
You can set config values via the Heroku CLI; for example, the following snippet uploads the TRELLO_API_KEY stored in your .env file:
```bash 
$ heroku config:set `cat .env | grep API_KEY`
```
Repeat the above for API_TOKEN and Board ID as well.

More information on Heroku capabilities can be found in [`https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime`](https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime)

####Step 2: Push an Image to Heroku
Heroku can't deploy images from Docker Hub directly, but instead uses its own (private) Docker registry. You need to push your image there, then tell Heroku to deploy it.
```bash
# Get the latest image from Docker Hub (built by your CI pipeline)
docker pull kiranuppi84/todo-app:prod
# Tag it for Heroku
docker tag kiranuppi84/todo-app:prod registry.heroku.com/ku-todo-app/web
# Login to Heruku Registry
echo "$HEROKU_API_KEY" | docker login --username="$HEROKU_USERNAME" --password-stdin registry.heroku.com
# Push it to Heroku registry
docker push registry.heroku.com/ku-todo-app/web
```

####Step 3: Release it to Heroku

```bash
heroku container:login
heroku container:release web --app ku-todo-app
```
#### Things to watch out for
* Note that Heroku requires your app to listen on a port defined by the $PORT environment variable in your .env file and Adjust your Dockerfile's ENTRYPOINT to execute a shell script which can read the $PORT value from your .env file.
* To authorise interaction with Heroku's API (such as heroku container:release web --app ku-todo-app ), set a HEROKU_API_KEY environment variable in Travis.

## Mongo DB
We are going to create a MongoDB cluster and configure our application to use it instead of Trello APIs. We are going to use a service called [`MongoDB Atlas`](https://www.mongodb.com/atlas/database). This will let us create a MongoDB cluster that our application can use.
Python support for MongoDB comes in the form of PyMongo. You can add this dependency to your project with poetry (or if your project uses pip to manage dependencies, you can use pip install instead of poetry add). Connecting to MongoDB Atlas has an additional dependency, so we also need to add pymongo[srv]:
```bash
poetry add pymongo pymongo[srv]
```
We need to add below Environment Variables in our .env, .env.test , travis and heroku configs
```bash
MONGODB_COLLECTION_NAME='Name of your MongoDB collection'
MONGO_DB_NAME='MongoDB database name'
MONGO_CONNECTION_STRING=mongodb+srv://<USER_NAME>:<PASSWORD>@cluster0.rgzrv.mongodb.net/ku13todo?retryWrites=true&w=majority

```
## Adding authentication and authorisation to the app
In order for us to protect our app being used freely by public, we are going to restrict by adding restrictions to our app using Github authentication through OAuth flow.
We need to register our to_do app for Github and install oauthlib and flask-login
```bash
 poetry add oauthlib flask-login
```

Todo App has Admin role and read roles. The very first user's github account against which app gets registered will become an Admin who can then change the roles for other users.
We need to add below Environment Variables in our .env, .env.test , travis and heroku configs
```bash
OAUTHLIB_INSECURE_TRANSPORT=1
LOGIN_DISABLED=True

GITHUB_CLIENT_ID=client-id
GITHUB_CLIENT_SECRET=client-secret
```

## Migrating application to single cloud platform

To-Do app has been migrated into a single cloud platform, Microsoft Azure. Here Flask App and database has been moved to Azure and production application, in a docker container, as an Azure App Service. 
ToDo App will now use Azure's CosmosDB, which has an API compatible with MongoDB. A webhook URL has been created and Post requests to this endpoint cause your app to restart and pull the latest version of the container image from the configured registry.
P.S : Make sure you update the Travis config to define WEBHOOK as a variable that gets read by the webhook.sh file.
You can access the Todo app by clicking on [`https://ku-todo-app.azurewebsites.net/`](https://ku-todo-app.azurewebsites.net/)

## Terraform 

Terraform has been used to declaratively describe our desired Azure infrastructure, and use that to deploy our todo-app with the same arrangement of Azure resources
Application and database have now been moved to Azure cloud using terraform. Travis deployment script has been updated to make use of terraform to perform deployments.
We need to set up service principal Authentication so that Travis can access and alter your azure resources. Once this has been set up, this will create an app registration with you as the owner.

We will also have to register new application  (thats hosted on Azure using terraform) for OAuth in github and have to define/update following environment variables in Travis to

  * ARM_CLIENT_ID
  * ARM_CLIENT_SECRET
  * ARM_SUBSCRIPTION_ID
  * ARM_TENANT_ID
  * GITHUB_CLIENT_ID
  * GITHUB_CLIENT_SECRET

The application can be accessed by clicking on [`https://production-ku-todo-app.azurewebsites.net/home`](https://production-ku-todo-app.azurewebsites.net/home)

## Loggly Integration
#### Loggly SetUp
Create a free trial account at Loggly [`https://www.loggly.com/`](https://www.loggly.com/). This will allow you to use all of Loggly's
features for 30 days. (After 30 days you should still be able to use most of the
features we set up here - the exception being the alerts set up in one of the
stretch goals)

Once you've created your account, log in and find the icon for "Logs" in the lefthand menu. Under this, select "Source Setup". Then, on the tabs along the top of
the page, select "Customer Tokens". Add a new customer token. Copy the value of the token and make a note of it, remembering that this is a secret token so should be managed in the same way as other sensitive config values.

Add a new config parameter to the app called LOGGLY_TOKEN and set it in
your .env file.

In our App, We're sending our logs to loggly using HTTPS. Make necessary changes to APP so that all the operations would be logged and sent to loggly.

Now go to Loggly and navigate to Logs > Log Explorer. Set the time range from 1
day in the past until now, and click Search. You should see your logs.
P.S : Make sure you add the same env variable in Travis to make build run without any issues

## Running Application on MiniKube
Minikube is a version of Kubernetes that you can run locally on a development machine

#### Installation and Configuration 
Please follow the steps mentioned in [`https://minikube.sigs.k8s.io/docs/start/`](https://minikube.sigs.k8s.io/docs/start/) to install and start minikube on your machine
Create an image of ToDo application and push it to MiniKube

```bash
docker build --target production --tag todo-app:prod .
minikube image load
```

Now run 
```bash
kubectl apply -f deployment.yaml
```
Make sure you dont see any error running the pod by running
```bash
kubectl get pods 
```
#### Creating Kubernetes secrets for deployments

```bash
kubectl create secret generic longly-token --from-literal=LOGGLY_TOKEN=<TOKEN_VALUE>
```

After each deployment, we need to run below command to link up our minikube Service with a port on localhost

```bash
kubectl port-forward service/module-14 5000:80 
```
#### Troubleshooting tips when dealing with minikube
If you want to know if the deployment configs are correct or not
```bash
kubectl describe pods
```
If the pod is up and running and app isn't working then you can run

```bash
kubectl logs <pod_name>
```
Please make sure you have all the variables in the .env file has been defined in deployment.yaml 