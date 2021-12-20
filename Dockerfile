# syntax=docker/dockerfile:1

FROM python:3.9.6

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV CONTAINER_VERSION=1.0

CMD ["python3", "tests/test.py"]
