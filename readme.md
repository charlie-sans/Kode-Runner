# CodeRunner

Welcome to Runner! the interactive code enviroment brought to you by OpenStudio!

Runner is a simple, yet powerful tool that allows you to run code in a variety of languages, and see the output in real time. It's perfect for testing out code snippets, or for running scripts.

## Usage

clone the repo and cd into the runner directory.

run /lib/server.py on a linux system. sorry windows.
spawn out Code from Charlie's public folder inside of a world in resonite and hit the purple button to connect to the server.
once you hear tada.wav, you are connected and can start running code.

type the code inside the main code box or drop one of the demo code files into the import area under the left monitor and click the green run button at the top right hand side of the window.
the output will appear in the output window on the left monitor.

this assumes that the UI theme issue hasn't been completed yet or you are using the default client included with the server.

password authentication with `-p {password}` or `--password {password}` 

## Features

- Run code in a variety of languages, including Python, C, C++, and more
- See the output in real time
- Fully interactive terminal
- Run code in a safe, isolated environment using Docker
- Easy to use, with a simple and intuitive interface

- Password authentication.

best part about this, is that it is all open source and free to use!

if your docker container gets destroyed, you can rebuild it by running the following command in the runner directory:

```bash
docker build -t runner .
```

this will rebuild the docker container and you can run the server again.


## Contributing

If you would like to contribute to Runner, please feel free to fork the repository and submit a pull request. We welcome contributions of all kinds, including bug fixes, new features, and improvements to the documentation.

if you need more infomation, please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## what is this?

ever wondered if you could literly type out text based languages inside of resonite and it just works?

well now you can!

code runner is a hardware/server duo that allows you to run python, c, c++ ect within resonite while still including the goodies such as watching cargo run take 24 hours because tokio hung itself for the 20th time today.

code features a fully interactive terminal that allows you to run anything you wish*

runner works through a docker container to run the code directly inside the docker container for safety and proformance*

## how does it work?

using websockets and a python server, we can run code inside of a docker container and send the output back to the client in real time.

this also allows for streaming a terminal to the client, allowing for a fully interactive terminal experience.

:DISCLAMER:
please know that this can allow arbatrary code execution on your system in the included docker container.
though it is running inside the container, just put caution.
:DISCLAMER:
