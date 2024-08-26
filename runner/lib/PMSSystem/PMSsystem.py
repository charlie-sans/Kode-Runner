import pexpect 
import json 
import os
import websockets
import asyncio
import re
import sys
from config import config


### START
async def execute_code(cmmand, websocket):
    child = pexpect.spawn(command, encoding="utf-8")
    while True:
        try:
            index = child.expect(['\n', '.', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                #coded_text = translate_terminal_colors(child.before)
                await websocket.send(child.after)
            elif index == 2:
                break
        except pexpect.exceptions.TIMEOUT:
            break
    os.remove(TEMP_BASH_FILE)

async def Write_code_Buffer(websocket, path):
    print("PMS Code")
    print("Path: " + path)
    print("Websocket: " + str(websocket))
    while True:
        code = await websocket.recv()
        parsed_code = json.loads(code)
        print("Code: " + str(parsed_code))
        filename = parsed_code["File_Name"]
        filecontents = parsed_code["File_Contents"]
        # get the file extention from the name 
        fileext = re.split(r"\.", filename)[1]
        with open("code/" + filename, "w") as f:
            f.write(filecontents)
        await websocket.send("File saved successfully " + filename)
        

async def Read_PMS_File(websocket, path):
    print("PMS File")
    print("Path: " + path)
    print("Websocket: " + str(websocket))
    while True:
        code = await websocket.recv()
        parsed_code = json.loads(code)
        print("Code: " + str(parsed_code))
        Sysver = parsed_code["PMS_System"]
        Project_name = parsed_code["Project_Name"]
        Entry_point = parsed_code["Main_File"]
        Output_Name = parsed_code["Project_Output"]
        Project_Build_System = parsed_code["Project_Build_System"]
        print("System Version: " + Sysver)
        print("Project Name: " + Project_name)
        print("Entry Point: " + Entry_point)
        print("Output Name: " + Output_Name)
        print("Project Build System: " + Project_Build_System)
        
        # Create the project directory
        os.system("mkdir " + Project_name)
        # Copy the files to the project directory
        os.system("cp code/* " + Project_name)
        
        # make a list of the varibles we parsed from the JSON
        project_vars = [Sysver, Project_name, Entry_point, Output_Name, Project_Build_System]
        # write the project vars to a file
        with open(Project_name + "/project_vars.json", "w") as f:
            f.write(json.dumps(project_vars))
            
        await websocket.send("Project saved successfully " + Project_name)
        await websocket.send("Project vars saved successfully " + Project_name)
        await websocket.send("Running PMS System")
        Run_PMS_system()
        
        
# init cmake
def init_cmake(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    Project_Build_System = project_vars[4]
    # create the CMakeLists.txt file
    with open(Project_name + "/CMakeLists.txt", "w") as f:
        f.write("cmake_minimum_required(VERSION 3.10)\n")
        f.write("project(" + Project_name + " VERSION 1.0)\n")
        f.write("add_executable(" + Output_Name + " " + Entry_point + ")\n")
    # create the build directory
    os.system("mkdir " + Project_name + "/build")
    # run cmake
    execute_code("cd " + Project_name + "/build && cmake ..", websocket)
    # run make
    execute_code("cd " + Project_name + "/build && make", websocket)
    # run the program
    execute_code("cd " + Project_name + "/build && ./" + Output_Name, websocket)
        
async def Run_PMS_system(websocket, path):
    print("Running PMS System")
    print("Path: " + path)
    print("Websocket: " + str(websocket))
    while True:
        # get the project vars
        with open(Project_name + "/project_vars.json", "r") as f:
            project_vars = json.loads(f.read())
        Sysver = project_vars[0]
        Project_name = project_vars[1]
        Entry_point = project_vars[2]
        Output_Name = project_vars[3]
        Project_Build_System = project_vars[4]
        # run the PMS system
        match Project_Build_System:
            case "cmake":
                init_cmake(project_vars,websocket)
            case "make":
                pass
            case "ant":
                pass
            case "gradle":
                pass
            case "maven":
                pass
            case "npm":
                pass
            
async def PMS(websocket, path):
    # main function for the PMS system
    print("PMS System")
    print("Path: " + path)
    print("Websocket: " + str(websocket))
    
    while True:
