# big size, no vulnerabilities, updated frequently
FROM python:3.9-slim

MAINTAINER Ever Alfonso García Méndez

WORKDIR elasticsearch-logs-container

COPY  . .

RUN pip3 install -r requirements.txt

EXPOSE 33

ENTRYPOINT ["python3", "./src/app.py"]
