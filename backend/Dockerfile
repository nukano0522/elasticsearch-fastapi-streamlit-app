FROM python:3.8-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src
COPY api ./src

# MeCab
RUN apt-get -y update && apt-get -y install mecab
RUN pip3 install unidic
RUN python -m unidic download

# Python library
RUN pip3 install --upgrade pip
RUN pip3 install fastapi
RUN pip3 install "uvicorn[standard]"
RUN pip3 install requests
RUN pip3 install elasticsearch==7.13.4
RUN pip3 install mecab-python3
RUN pip3 install gensim==3.8.0
# RUN pip3 install transformers

# RUN pip3 install streamlit

# ENTRYPOINT [ "python",  "./download.py"]
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
