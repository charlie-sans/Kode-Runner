import pexpect 
import json as jsthing
import os
import websockets
import asyncio
import re
import sys
from config import config

# CodeRunner PMS System

# This is the main function that will be called by the CodeRunner when the project is run

# example json b
# {
#     "PMS_System": "1.0",
#     "Project_Name": "<Project Name>",
#     "Project_Files": [{
#             "File_Name": "main.cpp",
#             "File_Extention": ".cpp"
#             },
#         {
#             "File_Name": "test.pms",
#             "File_Extention": ".pms"
#             }
#     ],
#     "Project_Build_System": "Rust",
#     "Project_Output": "main.exe",
#     "Project_Use_Multiple_Build_Systems": false,
#     "Project_Build_Systems": [{
#         "Build_System_Name": "Rust",
#         "Build_System_Arguments": [{
#                 "Argument_Type": "string",
#                 "Argument_Value": "c++"
#             },
#             {
#                 "Argument_Type": "json",
#                 "Argument_Value2": "test.pms"
#             },
#             {
#                 "Argument_Type": "string",
#                 "Argument_Value1": "main.exe"
#             },
#             {
#                 "Argument_Type": "bool",
#                 "Argument_Value1": false
#             }
#         ]
#     }],
#     "Project_Use_Language_Server_Protocol": false,
#     "Project_Language_Server_Protocol": {
#         "Language_Server_Protocol_Name": "LSP",
#         "Language_Server_Protocol_Version": "1.0",
#         "Language_Server_Protocol_Support": [{
#                 "Support_Type": "Code_Completion",
#                 "Support_Value": true
#             },
#             {
#                 "Support_Type": "Error_Checking",
#                 "Support_Value": true
#             }
#         ]
#     },
#     "Project_Error_Handling": {
#         "Error_Handling_Type": "Client",
#         "Error_Handling_Support": true
#     },
#     "Project_Code_Completion": {
#         "Code_Completion_Type": "Client",
#         "Code_Completion_Support": true
#     },
#     "Project_Multiple_Files_Support": {
#         "Multiple_Files_Type": "Client",
#         "Multiple_Files_Support": true
#     },
#     "Project_GUI": {
#         "GUI_Type": "Client",
#         "GUI_Style": [{
#                 "Style_Type": "Jetbrains",
#                 "Is_active": true
#             },
#             {
#                 "Style_Type": "Visual_Studio",
#                 "Is_active": false
#             },
#             {
#                 "Style_Type": "Visual_Studio_Code",
#                 "Is_active": false
#             }
#         ]
#     }
# }

# this is a comment 

PMSProjectFiless = "main.c"
Run_After_Build = False
conf = config()
class PMSSystem:
    def __init__(self) -> None:
        self.PMSVersion = conf.PMSVersion
        self.PMSProjectName = ""
        self.PMSProjectFiles = []
        self.PMSProjectLocation = "code"
        self.PMSProjectBuildSystem = ""
        self.PMSProjectOutput = []
        self.buildsystemcmds = []
        self.cmdargs = []
        self.jsonInput = []
        self.arguments = []
        self.PMSVersion = []
        self.PMSProjectName = []
        self.PMSProjectFiles = []
        self.PMSProjectBuildSystem = [] 
        self.PMSProjectOutput = []
        self.PMSProjectUseMultipleBuildSystems = False 
        self.PMSProjectBuildSystems = []
        self.PMSProjectUseLanguageServerProtocol = False
        self.PMSProjectLanguageServerProtocol = []
        self.PMSProjectErrorHandling = False
        self.PMSProjectCodeCompletion = False
        self.PMSProjectMultipleFilesSupport = False
        self.PMSProjectGUI = []
        if self.PMSVersion != conf.PMSVersion:
            print("Error: The PMS version is not supported, are you using the correct version of the CodeRunner?")
            return
            
     
     
 
        
                
    def assign(data,websocket):
        # we parse the json data, get the project name, files, build system, output, and build system arguments
        # we then set the values to the class variables
        # then we call the setup_build_system function to setup the build system
        
        parsed_data = jsthing.loads(data)
        PMSSystem.PMSVersion = parsed_data["PMS_System"]
        PMSSystem.PMSProjectName = parsed_data["Project_Name"]
        PMSProjectFiless = parsed_data["Main_File"]
        Run_After_Build = parsed_data["Run_On_Build"]
        PMSSystem.PMSProjectBuildSystem = parsed_data["Project_Build_Systems"]
        PMSSystem.PMSProjectOutput = parsed_data["Project_Output"]
        # print the parsed data so that we know that we have it.
        print("PMS Version: " + PMSSystem.PMSVersion)
        print("Project Name: " + PMSSystem.PMSProjectName)
        print("Project Files: " + str(PMSProjectFiless))
        print("Project Build System: " + PMSSystem.PMSProjectBuildSystem)
        print("Project Output: " + str(PMSSystem.PMSProjectOutput))
        
        # get the build system arguments
        if parsed_data["Project_Use_Multiple_Build_Systems"]:
            PMSSystem.PMSProjectUseMultipleBuildSystems = parsed_data["Project_Use_Multiple_Build_Systems"]
            print("Project Use Multiple Build Systems: " + str(PMSSystem.PMSProjectUseMultipleBuildSystems))
        if parsed_data["Project_Build_Systems"] != [] :
            PMSSystem.PMSProjectBuildSystems = parsed_data["Project_Build_Systems"]
            
        
        PMSS = PMSSystem.PMSProjectBuildSystem
        if PMSS == "cmake":
            # simple cmake build system
            clear("code/")
            with open("code/CMakeLists.txt", "w") as f:
                f.write("cmake_minimum_required(VERSION 3.10)\n")
                f.write("project(" + system.PMSProjectName + ")\n")
                f.write("add_executable(" + system.PMSProjectName + " " + str(PMSProjectFiless) + ")\n")
                print("cat " + str(PMSProjectFiless))
            execute_build_system( system, "cmake code/ && make")
            
     
            
    async def PMSCode(websocket, path):
        print("PMS Code")
        print("Path: " + path)
        print("Websocket: " + str(websocket))
        while True:
            code = await websocket.recv()
            parsed_code = jsthing.loads(code)
            print("Code: " + str(parsed_code))
            filename = parsed_code["File_Name"]
            filecontents = parsed_code["File_Contents"]
            # get the file extention from the name 
            fileext = re.split(r"\.", filename)[1]
            with open("code/" + filename, "w") as f:
                f.write(filecontents)
            await websocket.send("File saved successfully " + filename)
            

    async def PMSSystemStartup(websocket, path):
        print("PMS System Startup")
        print("Path: " + path)
        print("Websocket: " + str(websocket))
        
        while True:
            data = await websocket.recv()
            print("Data: " + data)
            PMSSystem.assign(data,websocket)
            await websocket.send("PMS System started successfully")
            await websocket.send("[H")
            await websocket.send("Project Name: " + PMSSystem.PMSProjectName)
            await websocket.send(" \n")
            await server(websocket, path)
            
            
            
async def execute_build_system( websocket,command):
    print( "Executing  build system", "INFO")
    
    #if not check_code_safety(code, websocket):
     #   await websocket.send("Unsafe code detected.")
      #  os.remove(TEMP_PYTHON_FILE)
       # return
    print("PMSSystem.PMSProjectName")
    print(PMSSystem.PMSProjectName)
    child = pexpect.spawn(command, encoding="utf-8")

    while True:
        try:
            index = child.expect(['.', '\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                await websocket.send(child.after)
            elif index == 2:
                #await websocket.send(child.before)
                break
        except pexpect.exceptions.TIMEOUT as e:
            de_bug( f"Execution timed out {e}", "ERROR")
            break
async def execute_code( websocket):
    print( "Executing  code", "INFO")
    
    #if not check_code_safety(code, websocket):
     #   await websocket.send("Unsafe code detected.")
      #  os.remove(TEMP_PYTHON_FILE)
       # return
    print("PMSSystem.PMSProjectName")
    print(PMSSystem.PMSProjectName)
    child = pexpect.spawn(f"./" + PMSSystem.PMSProjectName, encoding="utf-8")

    while True:
        try:
            index = child.expect(['.', '\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                await websocket.send(child.after)
            elif index == 2:
                #await websocket.send(child.before)
                break
        except pexpect.exceptions.TIMEOUT as e:
            de_bug( f"Execution timed out {e}", "ERROR")
            break


async def server(websocket, path):
    try:

        await execute_code( websocket)
    except websockets.exceptions.ConnectionClosedOK as e: 
        print("exiting")
        pass