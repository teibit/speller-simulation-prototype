# Dockerfile for archiver container.

# Build image from latest Python base.
FROM python

MAINTAINER Ever Alfonso García Méndez

# Containers have a file system of their own, which we'll interact with upon
# setting the image. The ~/app directory is our basement.
WORKDIR app

# Create directory structure.
RUN mkdir -p src/common
RUN mkdir -p sql

# Copy local files into the container's locations.
COPY src/containers/archiver/src/archiver.py .
COPY src/containers/archiver/requirements.txt .
COPY src/common src/common
COPY sql sql

# Notice that the file structure inside the container does not match that of
# the project locally. The ~/app directory directly contains this container's
# source code (archiver.py), the requirements file, and the src/common
# subdirectory. It does not contain code from any other container, nor
# anything else it doesn't strictly need.

# Install python3 requirements through pip3.
RUN pip3 install --no-cache-dir -r requirements.txt

# Command to run upon container creation.
# Note: the -u flag allows for unbuffered stdout.
ENTRYPOINT ["python3", "-u", "archiver.py", "MySQL"]

# Ignore warnings.
ENV PYTHONWARNINGS="ignore"
