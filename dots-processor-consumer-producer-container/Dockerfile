# big size, no vulnerabilities, updated frequently
FROM python:3.9-slim

MAINTAINER Ever Alfonso García Méndez

WORKDIR dots-processor-consumer-producer-container

COPY  . .

RUN pip3 install -r requirements.txt

EXPOSE 27

ENTRYPOINT ["python3", "./src/app.py"]
