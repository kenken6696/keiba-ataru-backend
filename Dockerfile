FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install tree
RUN mkdir -p /code
RUN mkdir -p /code/static
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/