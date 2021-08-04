poetry run gunicorn  --bind 0.0.0.0:$PORT "todo_app.app:create_app()"
#poetry run gunicorn todo_app.app:create_app --bind 0.0.0.0:8000
#poetry run flask run --host 0.0.0.0 --port 8082
