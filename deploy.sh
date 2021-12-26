#!/bin/bash
#docker pull $DOCKER_USERNAME/todo-app-prod:latest
#docker tag $DOCKER_USERNAME/todo-app-prod:latest registry.heroku.com/ku-todo-app/web
#echo "$HEROKU_API_KEY" | docker login --username="$HEROKU_USERNAME" --password-stdin registry.heroku.com
#docker push registry.heroku.com/ku-todo-app/web
#heroku container:login
#heroku container:release web --app ku-todo-app

terraform init
terraform apply -var "prefix=prod" -var "location=uksouth" -var "resource_group_name=OpenCohort1_KiranUppinkudru_ProjectExercise" -var "DOCKER_REGISTRY_SERVER_USERNAME='$DOCKER_USERNAME'" -var "DOCKER_REGISTRY_SERVER_PASSWORD='$DOCKER_PASSWORD'" -var "GITHUB_CLIENT_ID='$GITHUB_CLIENT_ID'" -var "GITHUB_CLIENT_SECRET='$GITHUB_CLIENT_SECRET'" -var "MONGODB_COLLECTION_NAME='$
MONGODB_COLLECTION_NAME'" -var "SECRET_KEY='$SECRET_KEY'" -auto-approve
export MONGO_CONNECTION_STRING="$(terraform output -raw cosmos_connection_string)"
echo "$MONGO_CONNECTION_STRING"
docker run -e MONGO_CONNECTION_STRING -e MONGODB_COLLECTION_NAME -e SECRET_KEY -e GITHUB_CLIENT_ID -e GITHUB_CLIENT_SECRET --entrypoint poetry todo-app-test:latest run pytest tests_e2e

