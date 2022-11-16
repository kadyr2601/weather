FROM python:3.10.1-alpine

# set work directory
WORKDIR /app/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev \
#    && pip install pipenv

## install dependencies
RUN pip install --upgrade pip

COPY ./req.txt /app/req.txt
RUN pip install -r /app/req.txt

COPY . /app/backend

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]