FROM python:3.9-buster as base
# Perform common operations, dependency installation etc...
RUN apt-get update && apt-get install -y \
    curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# Adding poetry to PATH
ENV PATH="/root/.poetry/bin:$PATH"

RUN mkdir /app/
COPY . /app/

# Defaults
WORKDIR /app/

#RUN poetry install
RUN poetry config virtualenvs.create false --local && poetry install --no-dev

FROM base as production
# Configure for production
CMD ["poetry" , "run", "gunicorn"  , "--bind", "0.0.0.0:8080", "todo_app.app:create_app()"]
EXPOSE 8080

FROM base as development
# Configure for local development
CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0" , "--port", "8080"]
EXPOSE 8080

FROM base as test
# Configure for local test
RUN apt-get update && \
    apt-get install -y gnupg wget unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /usr/local/bin/

RUN chmod +x /usr/local/bin/chromedriver
ENTRYPOINT ["poetry", "run", "pytest"]

