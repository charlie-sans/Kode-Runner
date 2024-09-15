#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
def run():
    print("Running the project...")
    # get the path of the script
    dir = os.path.dirname(__file__)
    # run the 2 servers 
    # run the web server
    web_server = subprocess.Popen(["dotnet", "run"], cwd=os.path.join(dir, "web"))
    # run the api server
    api_server = subprocess.Popen(["python3", "runner/main.py"], cwd=dir)
    print("Project complete.")

if __name__ == "__main__":
    run()