#!/bin/bash
poetry run gunicorn 'todo_app.app:create_app()' --bind "localhost:${PORT:-5000}"
