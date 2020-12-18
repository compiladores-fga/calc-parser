FROM python:3.7.0-slim

WORKDIR /home

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENTRYPOINT ["pytest"]
