# Python webserver
# Version: 1.0

# Pull base image
FROM ubuntu:latest

# Install python
RUN apt-get update -y && apt-get install -y python3-pip python3-dev python3-pexpect python3


COPY . /app
# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod 444 /app*
RUN chmod 777 /app/code

RUN useradd -r --shell /bin/sh limiteduser

USER limiteduser

ENTRYPOINT [ "/usr/bin/python3", "lib/server.py"]