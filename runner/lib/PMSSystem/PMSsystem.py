import pexpect 
import json 
import os
import websockets
import asyncio
import re
import sys
from config import config
import threading
import subprocess
import asyncio
import threading

### START
async def execute_code(command, websocket):
    print("Executing code")
    print("Command: " + command)
    child = pexpect.spawn(command, encoding="utf-8")
    while True:
        try:
            index = child.expect(['\n', '.', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                decolorised_text = re.sub(r'\x1b\[[0-9;]*m', '', child.after)
                await websocket.send(decolorised_text)
            elif index == 2:
                break
        except pexpect.exceptions.TIMEOUT:
            break

async def Write_code_Buffer(websocket, path):
    print("PMS Code")
    print("Path: " + path)
    print("Websocket: " + str(websocket))
    while True:
        code = await websocket.recv()
        # we got the code now, just got to check the first line for the project name in the languages comment
        # then we can save the code to the project directory
        
        # get the first line of the code
        first_line = code.split("\n")[0]
        print("First Line: " + first_line)
        print("seccond Line: " + code.split("\n")[1])
        print("Third Line: " + code.split("\n")[2])
        # check if the first line is a comment
        if first_line.startswith("#") or first_line.startswith("//") or first_line.startswith("/*") or first_line.startswith("<!--") or first_line.startswith("\"\"\""):
            # check if the comment has the filename in it
            if re.search("File_name: ", code.split("\n")[1]): # check if the comment has the filename in it
                # check if the comment has the project name in it
                if re.search("Project: ", code.split("\n")[2]):
                    # get the project name from the comment
                    project_name = code.split("\n")[2].split("Project: ")[1]
                    File_name = code.split("\n")[1].split("File_name: ")[1]
                    print("Project Name: " + project_name)
                    print("File Name: " + File_name)
                    # find the project directory if it exists
                    if os.path.exists(project_name):
                        # save the code to the project directory
                        with open(project_name + "/" + File_name, "w") as f:
                            f.write(code)
                            print("Code saved successfully")
                        await websocket.send(f"Code saved successfully to {project_name}/{File_name}\n")
                    else:
                        await websocket.send("<color=red>Error:</color> Project directory not found.\n")
                        # create the project directory
                        os.system("mkdir " + project_name)
                        await websocket.send("Project directory created")
                        # save the code to the project directory
                        with open(project_name + "/" + File_name, "w") as f:
                            f.write(code)
                            print("Code saved successfully\n")
                        await websocket.send(f"Code saved successfully to {project_name}/{File_name}\n")
                        
                        
                else:
                    await websocket.send("<color=red>Error:</color> Project name and filename not found in comment\n")
            else: 
                await websocket.send("<color=red>Error:</color> Filename not found in comment\n")
        else:
            await websocket.send("<color=red>Error:</color> Comment not found in code\n")
            
            
            
async def Read_PMS_File(websocket, path,code):
    print("PMS File")
    print("Path: " + path)
    print("Websocket: " + str(websocket))
 
      
    parsed_code = json.loads(code)
    print("Code: " + str(parsed_code))
    Sysver = parsed_code["PMS_System"]
    Project_name = parsed_code["Project_Name"]
    Entry_point = parsed_code["Main_File"]
    Output_Name = parsed_code["Project_Output"]
    Project_Build_System = parsed_code["Project_Build_Systems"]
    print("System Version: " + Sysver + "\n")
    print("Project Name: " + Project_name + "\n")
    print("Entry Point: " + Entry_point + "\n")
    print("Output Name: " + Output_Name + "\n")
    print("Project Build System: " + Project_Build_System + "\n")
    
    # Create the project directory
    os.system("mkdir " + Project_name)
    # Copy the files to the project directory
    os.system("cp code/* " + Project_name)
    
    # make a list of the varibles we parsed from the JSON
    project_vars = [Sysver, Project_name, Entry_point, Output_Name, Project_Build_System]
    # write the project vars to a file
    with open(Project_name + "/project_vars.json", "w") as f:
        f.write(json.dumps(project_vars))
        
    await websocket.send("Project named: " + Project_name + "saved successfully\n")
    await websocket.send("Project vars for " + Project_name + " saved successfully\n")
    await websocket.send("Running PMS System\n" )
    await Run_PMS_system(websocket,path,Project_name)
        
# imit node
async def init_node(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]  
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    print("Project Name: " + Project_name + "\n")
    print("Entry Point: " + Entry_point + "\n")
    print("Output Name: " + Output_Name + "\n")
    
    Project_Build_System = project_vars[4]
    # init node without npm as we dont need it
    await execute_code("node " + Project_name + "/" + Entry_point, websocket)
    
# init cmake
async def init_cmake(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]  
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    print("Project Name: " + Project_name + "\n")
    print("Entry Point: " + Entry_point + "\n")
    print("Output Name: " + Output_Name + "\n")
    
    Project_Build_System = project_vars[4]
    # create the CMakeLists.txt file
    with open(Project_name + "/CMakeLists.txt", "w") as f:
        f.write("cmake_minimum_required(VERSION 3.10)\n")
        f.write("project(" + Project_name + ")\n")
        f.write("add_executable(" + Output_Name + " " + Entry_point + ")\n")
    # create the build directory
    os.system("mkdir " + Project_name + "/build")
    print("CMakeLists.txt created\n")
    print("Build directory created\n")
    print("Running cmake\n")
    print(Project_name)
    print(Output_Name)
    # run cmake
    await execute_code("cmake -S " + Project_name + " -B " + Project_name + "/build", websocket)
    # # run make
    await execute_code("make -C " + Project_name + "/build", websocket)
    # # run the output
    await execute_code("./" + Project_name + "/build/" + Output_Name, websocket)    
        
async def Run_PMS_system(websocket, path,Project_name):
    print("Running PMS System\n")
    print("Path: " + path + "\n")
    print("Websocket: " + str(websocket) + "\n")

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
            await init_cmake(project_vars,websocket)
        case "make":
            await execute_code("make " + Project_name + "/" + Entry_point, websocket)
            await execute_code("./" + Project_name + "/" + Output_Name, websocket)
        case "ant":
            pass
        case "gradle":
            pass
        case "maven":
            pass
        case "node":
            await init_node(project_vars,websocket)
        case "yarn":    
            pass    
        case "python":
            await execute_code("python3 " + Project_name + "/" + Entry_point, websocket)
        case "cargo":
            pass
        case "rustc":
            await execute_code("rustc " + Project_name + "/" + Entry_point + " -o " + Project_name + "/" + Output_Name, websocket)
            await execute_code("./" + Project_name + "/" + Output_Name, websocket)
        case "go":
            pass
        case "dotnet":
            pass
            
            
            
async def PMS(websocket, path):
    # main function for the PMS system
    print("PMS System")
    print("Path: " + path)
    print("Websocket: " + str(websocket))
    

    code = await websocket.recv()
    parsed_code = json.loads(code)
    print("Code: " + str(parsed_code))
    await Read_PMS_File(websocket,path, code)
        