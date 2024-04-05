# Python webserver
# Version: 1.0

# Pull base image
FROM ubuntu:latest

# Install python
RUN apt update -y
RUN gpg --homedir /tmp --no-default-keyring --keyring /usr/share/keyrings/mono-official-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
RUN echo "deb [signed-by=/usr/share/keyrings/mono-official-archive-keyring.gpg] https://download.mono-project.com/repo/ubuntu stable-focal main" | tee /etc/apt/sources.list.d/mono-official-stable.list

RUN apt update -y && apt-get install -y python3-pip python3-dev python3-pexpect python3 htop iproute2 lua5.3 nodejs mono-devel gnuplot
COPY . /app
# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install websockets
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000



