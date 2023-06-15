FROM python:3.9-buster

ENV WORKDIR = /App/
WORKDIR $WORKDIR

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile* ./
RUN pipenv install --deploy
COPY index.py index.py
COPY assets assets
COPY app.py app.py
COPY core core
COPY db db
COPY database.conf .env
COPY layouts layouts
COPY callbacks callbacks
COPY conf_stations.json conf_stations.json
RUN python -c "from app import db; db.create_all()"
