# big size, no vulnerabilities, updated frequently
FROM python:3.9-slim

MAINTAINER Ever Alfonso García Méndez

WORKDIR kafka-consumer-container

COPY  . .

RUN pip3 install -r requirements.txt

EXPOSE 20

ENTRYPOINT ["python3", "./src/app.py"]

