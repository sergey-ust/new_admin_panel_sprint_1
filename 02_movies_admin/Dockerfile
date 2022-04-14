
FROM python:3.9-alpine

WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install 
RUN apk update

# install dependencies
COPY req_3_9.txt /app/req_3_9.txt

RUN pip install --no-cache-dir --upgrade pip &&\
 pip install --no-cache-dir -r req_3_9.txt &&\
 pip install --no-cache-dir gunicorn==20.1.0


COPY . .
