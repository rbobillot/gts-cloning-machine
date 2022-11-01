# Dockerfile

# pull the official docker image
FROM python:3.10.6

# set work directory
WORKDIR /gts-event-manager

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 8083