#!/bin/bash
poetry run gunicorn 'todo_app.app:create_app()' --bind "0.0.0.0:${PORT:-5000}"
