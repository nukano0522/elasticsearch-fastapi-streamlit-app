FROM python:3.8-buster

WORKDIR /src
COPY app ./src

# Python library
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install streamlit

ENTRYPOINT ["streamlit", "run", "main.py"]
