#!/bin/bash
poetry run gunicorn 'todo_app.app:create_app()' --bind "127.0.0.1:${PORT:-5000}"
