#!/usr/bin/env python3
import os 
import sys
dir = os.path.dirname(__file__)
def build():
    print("Building the project...")
    os.system("cd " "web && dotnet publish -c Release")
    # make the build folder
    os.system("mkdir output")
    # copy the output to the output folder
    os.system("cp -r web/bin/Release/net8.0/publish output")
    print("Build complete.")
    
if __name__ == "__main__":
    build()