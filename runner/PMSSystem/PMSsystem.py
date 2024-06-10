import json
import os
import websockets
import asyncio
from ..config.config import config

# CodeRunner PMS System

# This is the main function that will be called by the CodeRunner when the project is run

# example json
# {
#     "PMS_System": "1.0",
#     "Project_Name": "<Project Name>",
#     "Project_Files": [{
#             "File_Name": "main.cpp",
#             "File_Extention": ".cpp"
#         },
#         {
#             "File_Name": "test.pms",
#             "File_Extention": ".pms"
#         }
#     ],
#     "Project_Build_System": "Rust",
#     "Project_Output": "main.exe",
#     "Project_Use_Multiple_Build_Systems": false,
#     "Project_Build_Systems": [{
#         "Build_System_Name": "Rust",
#         "Build_System_Arguments": [{
#                 "Argument_Type": "string",
#                 "Argument_Value": "cpp"
#             },
#             {
#                 "Argument_Type": "json",
#                 "Argument_Value1": "main.cpp",
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

conf = config()
class PMSSystem:
    def __init__(self, json_file) -> None:
        self.PMSVersion = conf.PMSVersion
        self.PMSProjectName = ""
        self.PMSProjectFiles = []
        self.PMSProjectBuildSystem = ""
        self.PMSProjectOutput = ""
        self.buildsystemcmds = []
        self.cmdargs = ""
        self.jsonInput = {}
        self.arguments = {}
        self.jPMSVersion = json_file["PMS_System"]
        self.jPMSProjectName = json_file["Project_Name"]
        self.jPMSProjectFiles = json_file["Project_Files"]
        self.jPMSProjectBuildSystem = json_file["Project_Build_System"]
        self.jPMSProjectOutput = json_file["Project_Output"]
        self.jPMSProjectUseMultipleBuildSystems = json_file["Project_Use_Multiple_Build_Systems"]
        self.jPMSProjectBuildSystems = json_file["Project_Build_Systems"]
        self.jPMSProjectUseLanguageServerProtocol = json_file["Project_Use_Language_Server_Protocol"]
        self.jPMSProjectLanguageServerProtocol = json_file["Project_Language_Server_Protocol"]
        self.jPMSProjectErrorHandling = json_file["Project_Error_Handling"]
        self.jPMSProjectCodeCompletion = json_file["Project_Code_Completion"]
        self.jPMSProjectMultipleFilesSupport = json_file["Project_Multiple_Files_Support"]
        self.jPMSProjectGUI = json_file["Project_GUI"]
        
    def setup_build_system(PMSBuildSystemName):
        PMSS = PMSBuildSystemName
        if PMSS == "Coderunner-Tools":
            print("Setting up the build system")
            print("Build System Name: " + PMSBuildSystemName)
            print("supported Build System Arguments: " + str(conf.supportedBuildSystemsArguments))
            print("Build System Parsed Arguments: " + str(PMSSystem.arguments))
            
            
            if PMSSystem.arguments == {}:
                print("Error: The build system arguments are not set, please set them in the pms file.")
                return
            else:
                with open("build.sh") as f:
                    f.write("#!/bin/bash\n")
                    f.write("echo 'Building the project...'\n")
                    f.write("echo 'Build System Name: " + PMSBuildSystemName + "'\n")
                    f.write("echo 'Build System Arguments: " + str(PMSSystem.arguments) + "'\n")
                    f.write("echo 'Build System Parsed Arguments: " + str(PMSSystem.arguments) + "'\n")
                    f.write("echo 'Build System complete'\n")
                    f.write("building Project\n")
                    for arguments in PMSSystem.arguments:
                        # split the arguments and join them back together on a space
                        arguments = " ".join(arguments.split())
                        print("Building Project with arguments: " + arguments)
                        PMSSystem.buildsystemcmds.append(PMSSystem.buildsystemcmd + " " + arguments)
                    f.write("echo 'Building Project with arguments: " + arguments + "'\n")
                    f.write(PMSSystem.buildsystemcmds)
                    f.write("echo 'Project built successfully'\n")
                
                print("Build System setup complete")
    def setup_multiple_build_systems(PMSBuildSystems):
        pass

        
        
    def setup_language_server_protocol(PMSLanguageServerProtocolName, PMSLanguageServerProtocolVersion, PMSLanguageServerProtocolSupport):
        PMSLSP = PMSLanguageServerProtocolName
        PMSLSV = PMSLanguageServerProtocolVersion
        PMSLSS = PMSLanguageServerProtocolSupport

        if PMSLSV != conf.version:
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
        setup_language_server_protocol(PMSLanguageServerProtocolName, PMSLanguageServerProtocolVersion, PMSLanguageServerProtocolSupport)


    # sort the json file
    def sort_json(json_file):
        return json.dumps(json_file, indent=4, sort_keys=True)

    # read the json files contents and setup the build project
    def setup_project(json_file):
        if PMSProjectUseLanguageServerProtocol:
            # setup the language server
            setup_language_server(PMSProjectLanguageServerProtocol)
        elif PMSProjectUseMultipleBuildSystems:
            # setup multiple build systems
            self.setup_multiple_build_systems(PMSProjectBuildSystems)
        else:
            # setup the build system
            setup_build_system(PMSProjectBuildSystem)
    