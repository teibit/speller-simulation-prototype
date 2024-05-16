# big size, no vulnerabilities, updated frequently
FROM python:3.9-slim

MAINTAINER Ever Alfonso García Méndez

WORKDIR binary-processor-consumer-producer-container

COPY  . .

RUN pip3 install -r requirements.txt

EXPOSE 29

ENTRYPOINT ["python3", "./src/app.py"]
