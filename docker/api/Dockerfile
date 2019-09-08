FROM nvcr.io/nvidia/pytorch:19.07-py3
RUN apt update && apt install tree
RUN mkdir -p /code && mkdir -p /code/static
WORKDIR /code
ADD . /code/
RUN pip install -U pip && pip install -r requirements.txt