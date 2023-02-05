FROM python:3.9

WORKDIR /GraphApp

COPY src/main.py .

COPY src/templates/index.html ./templates/index.html

COPY src/templates/actors.html ./templates/actors.html

COPY src/templates/movies.html ./templates/movies.html

COPY src/templates/movies_actor.html ./templates/movies_actor.html

COPY src/templates/actors_movie.html ./templates/actors_movie.html

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

