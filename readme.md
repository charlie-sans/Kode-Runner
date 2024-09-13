# kode-Runner

Welcome to Runner! the interactive code enviroment brought to you by Finite

Runner is a simple, yet powerful tool that allows you to run code in a variety of languages, and see the output in real time. It's perfect for testing out code snippets, or for running scripts.

## Usage

using the releases of the runner docker container, pull the image then spin one of them up on port 5000.
ingame, spawn out the kode client or any supported client from `resrec:///G-pussafire/R-7EDF219CF4884A1144CBB4F2A9FA271C7581CF20BFCC7AA10624ECC84998F18D` and hit the purple colored connection button. 
after a few secconds, you should be connected!


## Features

- Run code in a variety of languages, including Python, C, C++, and more
- See the output in real time
- Fully interactive terminal
- Run code in a safe, isolated environment using Docker
- Easy to use, with a simple and intuitive interface

best part about this, is that it is all open source and free to use!


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

