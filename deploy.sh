#!/bin/bash
docker pull $dockerUsername/todo-app-prod:latest
docker tag $dockerUsername/todo-app-prod:latest registry.heroku.com/ku-todo-app/web
echo "$HEROKU_API_KEY" | docker login --username="$HEROKU_USERNAME" --password-stdin registry.heroku.com
heroku container:login
docker push registry.heroku.com/ss-todo-app/web
heroku container:release web --app ss-todo-app
