from debug import de_bug
import asyncio
import os
import sys
import requests
import json

class config:
    def __init__(self):
        self.runnerVersion = "2.0.0"
        self.langServerSuppport = False
        self.PMSVersion = "1.0"
        self.langServer = ""
        self.langServerVersion = ""
        self.langServerSupport = []
        self.langServerProtocolSupport = []
        self.langServerProtocolSupportType = []
        self.supportedLangServer = []
        self.supportedBuildSystems = []
        self.supportedBuiltinBuildSystems = ["Coderunner-Tools"]
        self.supportedBuildSystemsArguments = []
        
conf = config()
if conf.runnerVersion == "":
    de_bug("runnerVersion is not set, please set it in the config file.", "ERROR")
    sys.exit()


if __name__ == "__main__":
    async def main():
        await de_bug("hey! it's charlie, seems like your running this config file from the command line.", "ERROR")
        await de_bug("i know your more suited to running config files when you see them as they 'may setup your program'", "ERROR")
        await de_bug("but this file is a configuration file dedicated to storing varibles and some functions for the server.", "ERROR")
        await de_bug("by all means use this file inside one of your addons or projects, after all how else are you supppost to get the version.", "ERROR")
        await de_bug("take care!", "ERROR")
    asyncio.run(main())