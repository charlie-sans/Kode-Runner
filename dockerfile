# Python webserver
# Version: 1.0

# Pull base image
FROM ubuntu:20.04

# Install python
RUN apt update -y
ENV DEBIAN_FRONTEND=noninteractive


RUN apt update -y && apt-get install -y python3-pip python3-dev python3-pexpect python3 htop iproute2 lua5.3 nodejs mono-devel gnuplot lua5.3 luarocks cmake make gcc g++ libssl-dev libffi-dev python3-dev python3-pip python3-setuptools python3-venv python3-wheel python3-cffi
# Set the working directory in the container

# Install any needed packages specified in requirements.txt
RUN pip install websockets asyncio websockets colorama pyte termplotlib pexpect textual PySide6 requests


RUN apt-get install -y cmake 


# Make port 5000 available to the world outside this container
COPY . /app
WORKDIR /app
EXPOSE 5000

# run the server
CMD ["python3", "runner/main.py"]