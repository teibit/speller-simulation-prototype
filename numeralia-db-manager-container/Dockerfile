# big size, no vulnerabilities, updated frequently
FROM python:3.9-slim

MAINTAINER Ever Alfonso García Méndez

WORKDIR numeralia-db-manager-container

COPY  . .

RUN pip3 install -r requirements.txt

EXPOSE 30

ENTRYPOINT ["python3", "./src/app.py"]
