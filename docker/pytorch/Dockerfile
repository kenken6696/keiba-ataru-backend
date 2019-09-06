FROM nvcr.io/nvidia/pytorch:19.07-py3
RUN conda install numpy scipy scikit-learn pandas joblib
RUN apt update && apt -y install tree ipython3
RUN pip install -U pip && pip3 install deap update_checker tqdm stopit xgboost tpot logzero
RUN mkdir -p /code
RUN mkdir -p /code/static
WORKDIR /code
ADD . /code/