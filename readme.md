# Welcome to Kode-Runner, the interactive code environment brought to you by Finite!

Kode-Runner is a versatile tool that lets you run code in various languages and see the output in real-time. It’s ideal for testing code snippets or running scripts.
How to Use

- Get the Docker Image: Pull the Kode-Runner Docker image from the releases.
- Run the Docker Container: Start the container on port 5000.
- Connect to the Client: In resonite, spawn the Kode client or any supported client using the following URL: resrec:///G-pussafire/R-7EDF219CF4884A1144CBB4F2A9FA271C7581CF20BFCC7AA10624ECC84998F18D. Click the purple connection button.
- Connect: After a few seconds, you should be connected!

Features

- Multi-Language Support: Run code in languages like Python, C, C++, and more.
- Real-Time Output: See your code’s output as it executes.
- Interactive Terminal: Engage with a fully interactive terminal.
- Safe and Isolated: Runs code in a Docker container for security.
- User-Friendly: Simple and intuitive interface.
- Password authentication: Read password.md.

Best of all, Kode-Runner is open source and free to use!
Contributing

Want to contribute to Kode-Runner? Feel free to fork the repository and submit a pull request. We welcome contributions, including bug fixes, new features, and documentation improvements.

For more details, please check the CONTRIBUTING.md file.
What is Kode-Runner?

Have you ever wanted to execute text-based code inside Resonite? Now you can!

Kode-Runner is a hardware/server solution that allows you to run languages like Python, C, and C++ within Resonite. It includes features like real-time output and a fully interactive terminal.

Kode-Runner uses a Docker container to ensure safety and performance while running your code.
How Does It Work?

We utilize WebSockets and a Python server to execute code inside a Docker container and send the output back to the client in real-time. This setup allows for streaming a terminal to the client, providing a fully interactive coding experience.
