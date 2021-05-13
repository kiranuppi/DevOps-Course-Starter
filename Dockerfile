FROM python:3.9-buster as base
# Perform common operations, dependency installation etc...
RUN apt-get update && apt-get install -y \
    curl \
    git

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# Adding poetry to PATH
ENV PATH="/root/.poetry/bin:$PATH"

RUN mkdir /app/
COPY . /app/

# Defaults
WORKDIR /app/

RUN poetry install

FROM base as production
# Configure for production
CMD ["poetry" , "run", "gunicorn"  , "--bind", "0.0.0.0:8080", "todo_app.app:create_app()"]
EXPOSE 8080

FROM base as development
# Configure for local development
CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0" , "--port", "8080"]
EXPOSE 8080

FROM base as test
# Configure for local development
CMD ["poetry", "run", "pytest"]

