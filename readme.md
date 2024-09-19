# CodeRunner

Welcome to **CodeRunner**, an interactive code environment brought to you by OpenStudio! CodeRunner is a simple yet powerful tool that allows you to run code in various languages and view the output in real-time. It's perfect for testing code snippets or running scripts.

## What is CodeRunner?

Ever wondered if you could type out code directly inside **Resonite** and have it just work? Now you can!

CodeRunner is a hardware/server solution that lets you run various programming languages, like Python, C, and C++, directly inside Resonite. It even includes a fully interactive terminal where you can run any code you wish.

CodeRunner operates inside a Docker container to ensure safety and performance, giving you the freedom to execute code securely.

## Features

- **Multi-language Support**: Run code in Python, C, C++, and more.
- **Real-time Output**: See results instantly as you run your code.
- **Interactive Terminal**: Use a fully interactive terminal for real-time input and output.
- **Safe and Isolated Environment**: Code execution happens within a secure Docker container.
- **User-friendly Interface**: Simple and intuitive to use, even for beginners.
- **Open Source**: Free to use and contribute to!

## Setup and Usage

### 1. Cloning the Repository
First, clone the repo and navigate to the `runner` directory:
```bash
git clone https://github.com/charlie-sans/Kode-Runner.git
cd runner
```

### 2. Running CodeRunner
Run the main script on a Linux system or through WSL (Windows Subsystem for Linux):
```bash
python3 lib/main.py
```

Once CodeRunner is set up, spawn **Code from Charlie's public folder** inside a world in **Resonite**. Hit the purple button to connect to the server.

When you hear the `tada.wav` sound, you are successfully connected and can start running code.

### 3. Running Code
- **Type Code**: Type your code directly into the main code box.
- **Import Files**: Drop one of the demo code files into the import area under the left monitor.
- **Run Code**: Click the green run button in the top right corner of the window.
- **View Output**: Output will appear in the output window on the left monitor.

### 4. Rebuilding the Docker Container
If your Docker container gets destroyed, you can rebuild it by running:
```bash
docker build -t runner .
```
This will rebuild the container, and you can start the server again.

## Contributing

We welcome contributions! If you'd like to contribute to CodeRunner, feel free to fork the repository and submit a pull request. Contributions of all types are appreciated, whether it's bug fixes, new features, or improvements to the documentation.

For more details on contributing, check out the [CONTRIBUTING.md](https://github.com/charlie-sans/Kode-Runner/blob/dev/CONTRIBUTING.md) file.

## FAQ

### What is CodeRunner?
CodeRunner is a hardware/server duo that allows you to run various text-based programming languages (Python, C, C++, etc.) inside **Resonite**.

### How does it work?
Using WebSockets and a Python server, CodeRunner executes code inside a Docker container and streams the output back to the client in real-time. This creates a fully interactive terminal experience within the client.

### Is it safe?
While CodeRunner runs the code in an isolated Docker container for safety and performance, please be aware that it can allow arbitrary code execution within that container. Use caution when running untrusted code.
