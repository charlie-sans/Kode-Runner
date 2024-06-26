import json as jsthing
import os
import websockets
import asyncio
import re
import sys
from config import config

# CodeRunner PMS System

# This is the main function that will be called by the CodeRunner when the project is run

# example json
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
            
     
        
    def setup_build_system(system):
        PMSS = system.PMSProjectBuildSystem
        if PMSS == "Coderunner-Tools":
            print("Setting up the build system")
            print("Build System Name: " + PMSS)
            print("supported Build System Arguments: " + str(conf.supportedBuildSystemsArguments))
            print("Build System Parsed Arguments: " + str(PMSSystem.arguments))
            
            
            if PMSSystem.arguments == {}:
                print("Error: The build system arguments are not set, please set them in the pms file.")
                return
            else:
                with open("./build.sh") as f:
                    print("Build System complete, writing the commands to the file ")
                    f.write("#!/bin/bash\n")
                    f.write("echo 'Building the project...'\n")
                    f.write("echo 'Build System Name: " + PMSS + "'\n")
                    f.write("echo 'Build System Arguments: " + str(PMSSystem.arguments) + "'\n")
                    f.write("echo 'Build System Parsed Arguments: " + str(PMSSystem.arguments) + "'\n")
                    f.write("echo 'Build System complete'\n")
                    f.write("building Project\n")
                    for arguments in PMSSystem.arguments:
                        # split the arguments and join them back together on a space
                        arguments = " ".join(arguments.split())
                        print("Building Project with arguments: " + arguments)
                        system.buildsystemcmds.append(PMSSystem.buildsystemcmd + " " + arguments)
                    f.write("echo 'Building Project with arguments: " + arguments + "'\n")
                    f.write(PMSSystem.buildsystemcmds)
                    f.write("echo 'Project built successfully'\n")
                #os.system("chmod +x build.sh")
                #os.system("./build.sh")                
                
    def setup_multiple_build_systems(PMSBuildSystems):

        print("Setting up multiple build systems is not supported yet")

    
        
    def setup_language_server_protocol(PMSLanguageServerProtocolName, PMSLanguageServerProtocolVersion, PMSLanguageServerProtocolSupport):
        PMSLSP = PMSLanguageServerProtocolName
        PMSLSV = PMSLanguageServerProtocolVersion
        PMSLSS = PMSLanguageServerProtocolSupport

        if PMSLSV != conf.langServerVersion:
            print("Error: The language server protocol version is not supported, are you using the correct version of the CodeRunner?")
            return

        print("Setting up the language server protocol")
        print("Language Server Protocol Name: " + PMSLanguageServerProtocolName)
        print("Language Server Protocol Version: " + PMSLanguageServerProtocolVersion)
        print("Language Server Protocol Support: " + str(PMSLanguageServerProtocolSupport))
        #TODO: setup the language server protocol
        print("Language Server Protocol setup complete")
    def setup_build_system_protocol(PMSBuildSystemProtocolName, PMSBuildSystemProtocolVersion, PMSBuildSystemProtocolSupport):
        PMSB = PMSBuildSystemProtocolName
        PMSV = PMSBuildSystemProtocolVersion
        PMSS = PMSBuildSystemProtocolSupport

        if PMSV != conf.version:
            print("Error: The build system protocol version is not supported, are you using the correct version of the CodeRunner?")
            return

        print("Setting up the build system protocol")
        print("Build System Protocol Name: " + PMSBuildSystemProtocolName)
        print("Build System Protocol Version: " + PMSBuildSystemProtocolVersion)
        print("Build System Protocol Support: " + str(PMSBuildSystemProtocolSupport))
        print("Build System Protocol setup complete")

    def setup_language_server(json_file):
        PMSLanguageServerProtocolName = json_file["Language_Server_Protocol_Name"]
        PMSLanguageServerProtocolVersion = json_file["Language_Server_Protocol_Version"]
        PMSLanguageServerProtocolSupport = json_file["Language_Server_Protocol_Support"]

        # setup the language server
        #setup_language_server_protocol(PMSLanguageServerProtocolName, PMSLanguageServerProtocolVersion, PMSLanguageServerProtocolSupport)


    # sort the json file
    def sort_json(json_file):
        return jsthing.loads(json_file)

    def assign(json_file):
        print("Assigning the json file")
        
        json = json_file
        print("Json: " + str(json))
        projects = []
        system= PMSSystem()
        
        try:
            for project_file in json["Project_Files"]:
                # Extract and assign the values to variables
                file_name = project_file["File_Name"]
                file_extension = project_file["File_Extention"]
                system.PMSProjectFiles.append(file_name + file_extension)
        except KeyError:
            print("Error: The project files are not set, please set them in the pms file.")
           
        try:
            system.PMSProjectBuildSystem = json["Project_Build_Systems"][0]["Build_System_Name"]
            print("setting Build System: " + system.PMSProjectBuildSystem)
            #system.PMSProjectOutput = json["Project_Output"]
            system.PMSProjectUseMultipleBuildSystems = json["Project_Use_Multiple_Build_Systems"]
        except KeyError as k:
            print("Error: The project build system is not set, please set it in the pms file.")
            print(k)
            
        try:
            for project in json["Project_Build_Systems"]:
                system.PMSProjectBuildSystems.append(project["Build_System_Name"])
                system.PMSProjectUseLanguageServerProtocol = json["Project_Use_Language_Server_Protocol"]
        except KeyError:
            print("no project build systems set, please set them in the pms file.")
          
        try:
            for project in json["Project_Language_Server_Protocol"]:
                system.PMSProjectLanguageServerProtocol.append(project)
            system.PMSProjectErrorHandling = json["Project_Error_Handling"]
            system.PMSProjectCodeCompletion = json["Project_Code_Completion"]
            system.PMSProjectMultipleFilesSupport = json["Project_Multiple_Files_Support"]
            for project in json["Project_GUI"]:
                system.PMSProjectGUI.append(project)
            system.PMSProjectName = json["Project_Name"]
        except KeyError:
            print("Error: The project language server protocol is not set, please set it in the pms file.")
           
        if not os.path.exists(system.PMSProjectLocation):
            os.makedirs(system.PMSProjectLocation)
            
        #     print(f"File Name: {file_name}, File Extension: {file_extension}")
        # print("Project Files: " + str(system.PMSProjectFiles))
        # print("Project Build System: " + str(system.PMSProjectBuildSystem))
        # #print("Project Output: " + system.PMSProjectOutput)
        # print("Project Use Multiple Build Systems: " + str(system.PMSProjectUseMultipleBuildSystems))
        # print("Project Build Systems: " + str(system.PMSProjectBuildSystems))
        # print("Project Use Language Server Protocol: " + str(system.PMSProjectUseLanguageServerProtocol))
        # print("Project Language Server Protocol: " + str(system.PMSProjectLanguageServerProtocol))
        # print("Project Error Handling: " + str(system.PMSProjectErrorHandling))
        # print("Project Code Completion: " + str(system.PMSProjectCodeCompletion))
        # print("Project Multiple Files Support: " + str(system.PMSProjectMultipleFilesSupport))
        # print("Project GUI: " + str(system.PMSProjectGUI))
        # print("Project Name: " + str(system.PMSProjectName))
        # print("Project Location: " + str(system.PMSProjectLocation))
        # print("Assigning complete")
        data = f"""PMS System Started
        PMS Version: {system.PMSVersion}
        PMS Project Name: {system.PMSProjectName}
        PMS Project Files: {system.PMSProjectFiles}
        PMS Project Build System: {system.PMSProjectBuildSystem}
        PMS Project Output: {system.PMSProjectOutput}
        PMS Project Use Multiple Build Systems: {system.PMSProjectUseMultipleBuildSystems}
        PMS Project Build Systems: {system.PMSProjectBuildSystems}
        PMS Project Use Language Server Protocol: {system.PMSProjectUseLanguageServerProtocol}
        PMS Project Language Server Protocol: {system.PMSProjectLanguageServerProtocol}
        PMS Project Error Handling: {system.PMSProjectErrorHandling}
        PMS Project Code Completion: {system.PMSProjectCodeCompletion}
        PMS Project Multiple Files Support: {system.PMSProjectMultipleFilesSupport}
        PMS Project GUI: {system.PMSProjectGUI}
        PMS Project Name: {system.PMSProjectName}
        PMS Project Location: {system.PMSProjectLocation}
        PMS System setup complete
        setting up the build script
        """
        return data       
    # read the json files contents and setup the build project
    def setup_project(json_file):
        # sort the json file
        system = PMSSystem()
        system.jsonInput = PMSSystem.sort_json(json_file)
        # setup the project
      
        PMSSystem.assign(system.jsonInput)
        
        # if PMSSystem.jPMSProjectUseLanguageServerProtocol:
        #     # setup the language server
        #     PMSSystem.setup_language_server(PMSSystem.PMSProjectLanguageServerProtocol)
        # elif PMSSystem.PMSProjectUseMultipleBuildSystems:
        #     # setup multiple build systems
        #     PMSSystem.setup_multiple_build_systems(PMSSystem.PMSProjectBuildSystems)
        # else:
        #     # setup the build system
        PMSSystem.setup_build_system(system)
 
    async def PMSSystemStartup(websocket,path):
        PMSjson = await websocket.recv()
        PMSSystem.setup_project(PMSjson)
        system = PMSSystem()
        
       
    
        print("PMS System setup complete")
        
        
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
            with open(filename, "w") as f:
                f.write(filecontents)
            await websocket.send("File saved successfully " + filename)
            
