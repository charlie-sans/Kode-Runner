import pexpect 
import json 
import os
import websockets
import asyncio
import re
import klog
import sys
import config
import threading
import subprocess
import asyncio
import threading
import signal
import time

conf = config.config()
_debug_enabled = False
### START
stopped = False
current_process = None

async def execute_code(command, websocket):
    global current_process, stopped
    print("Executing code")
    print("Command: " + command)
    current_process = pexpect.spawn(command, encoding="utf-8")
    print(f"Process PID: {current_process.pid}")  # Print the PID of the current process
    while True:
        print(stopped)
        if stopped:
            await websocket.send("Process stopped\n")
            current_process.kill(signal.SIGSTOP)
            stopped = False  # Reset stopped to False
            break
        try:
            index = current_process.expect(['\n', '.', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                decolorised_text = re.sub(r'\x1b\[[0-9;]*m', '', current_process.after)
                await websocket.send(decolorised_text)
            elif index == 2:
                break
        except pexpect.exceptions.TIMEOUT:
            break

def stop_current_process():
    global stopped
    stopped = True
    if current_process:
        print(f"Stopping process with PID: {current_process.pid}")  # Print the PID of the process being stopped
        current_process.kill(signal.SIGSTOP)

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
        if _debug_enabled:
            klog.log("First Line: " + first_line)
            klog.log("Second Line: " + code.split("\n")[1])
            klog.log("Third Line: " + code.split("\n")[2])
        # check if the first line is a comment
        comment_patterns = [
            r"^#",
            
            r"^//",
            r"^/\*",
            r"^<!--",
            r"^\"\"\"",
            # for C 
            r"^\\*",
            r"^\/*",
            # for C++
            r"^//",
            r"^'''",
            r"^REM",  # For BASIC
            r"^;.*",  # For Lisp
            r"^%.*",  # For Prolog
            r"^--",   # For SQL, Ada
            r"^:.*",  # For AppleScript
            r"^--\[\[", # For Lua
        ]
        if any(re.match(pattern, first_line) for pattern in comment_patterns):
            # check if the comment has the filename in it
            if re.search("File_name: ", code.split("\n")[1]): # check if the comment has the filename in it
                # check if the comment has the project name in it
                if re.search("Project: ", code.split("\n")[2]):
                    # get the project name from the comment
                    project_name = code.split("\n")[2].split("Project: ")[1]
                    File_name = code.split("\n")[1].split("File_name: ")[1]
                    if _debug_enabled:
                        klog.log("Project Name: " + project_name)
                        klog.log("File Name: " + File_name)
                    # find the project directory if it exists
                    if os.path.exists(project_name):
                        # save the code to the project directory
                        with open(project_name + "/" + File_name, "w") as f:
                            f.write(code)
                            print("Code saved successfully")
                        await websocket.send(f"Code saved successfully to: {project_name}/{File_name}\n")
                    else:
                        await websocket.send("<color=red>Error:</color> Project directory not found.\n")
                        if _debug_enabled:
                            klog.error("Project directory not found")
                        # create the project directory
                        os.system("mkdir " + project_name)
                        await websocket.send("Project directory created\n")
                        # save the code to the project directory
                        with open(project_name + "/" + File_name, "w") as f:
                            f.write(code)
                            print("Code saved successfully\n")
                        await websocket.send(f"Code saved successfully to {project_name}/{File_name}\n")
                        
                        
                else:
                    await websocket.send("<color=red>Error:</color> Project name and filename not found in block comment\n")
                    klog.error("Project name and filename not found in block comment")
            else: 
                await websocket.send("<color=yellow>Warning:</color> Filename not found in comment,could it be a makefile?\n")
                print("Filename not found in comment, could it be a makefile?")
                # check if the file is a makefile
                
                # check for first line comment containing Makefile
                print("Checking for Makefile")
                print("First Line: " + first_line)
                if re.search("#Makefile", first_line):
                    # save the code to the project directory
                    project_name = code.split("\n")[1].split("Project: ")[1]
                    with open(project_name + "/Makefile", "w") as f:
                        f.write(code)
                        print("Code saved successfully")
                    await websocket.send(f"makefile saved successfully to: {project_name}/Makefile\n")
                    
        else:
            await websocket.send("<color=red>Error:</color> Comment not found in code\n")
            klog.error("Comment not found in code")
            
            
            
async def Read_PMS_File(websocket, path,code):

      
    parsed_code = json.loads(code)
    Sysver = parsed_code["PMS_System"]
    Project_name = parsed_code["Project_Name"]
    Entry_point = parsed_code["Main_File"]
    Output_Name = parsed_code["Project_Output"]
    Project_Build_System = parsed_code["Project_Build_Systems"]
    arguments = parsed_code["compiler-arguments"]
    _debug_enabled = parsed_code["Debug_enabled"]
  #java hello world
  # CodeRunner_libs_to_include = parsed_code["CodeRunner_include_libs"]
    if _debug_enabled:
        print("System Version: " + Sysver + "\n")
        print("Project Name: " + Project_name + "\n")
        print("Entry Point: " + Entry_point + "\n")
        print("Output Name: " + Output_Name + "\n")
        print("Project Build System: " + Project_Build_System + "\n")
    
    if os.path.exists(Project_name):
        pass
    else:
        
        # Create the project directory
        os.system("mkdir " + Project_name)
        # Copy the files to the project directory
        os.system("cp code/* " + Project_name)
    
    # make a list of the varibles we parsed from the JSON
    project_vars = [Sysver, Project_name, Entry_point, Output_Name, Project_Build_System, arguments, _debug_enabled]
    # write the project vars to a file
    with open(Project_name + "/project_vars.json", "w") as f:
        f.write(json.dumps(project_vars))
        
    await websocket.send("Project named: " + Project_name + " saved successfully\n")
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

# init g++
async def init_gpp(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]  
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    print("Project Name: " + Project_name + "\n")
    print("Entry Point: " + Entry_point + "\n")
    print("Output Name: " + Output_Name + "\n")
    
    Project_Build_System = project_vars[4]
    # init g++
    await execute_code("g++ " + Project_name + "/" + Entry_point + " -o " + Project_name + "/" + Output_Name, websocket)
    await execute_code("./" + Project_name + "/" + Output_Name, websocket)    

# init cargo
async def init_cargo(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]  
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    print("Project Name: " + Project_name + "\n")
    print("Entry Point: " + Entry_point + "\n")
    print("Output Name: " + Output_Name + "\n")
    
    Project_Build_System = project_vars[4]
    # init cargo through the cargo.toml file
    with open(Project_name + "/Cargo.toml", "w") as f:
        f.write("[package]\n")
        f.write("name = \"" + Project_name + "\"\n")
        f.write("version = \"0.1.0\"\n")
        f.write("edition = \"2018\"\n")
        f.write("[dependencies]\n")
    # run cargo
    await execute_code("cargo run", websocket)
    
    
# init mono
async def init_mono(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]  
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    print("Project Name: " + Project_name + "\n")
    print("Entry Point: " + Entry_point + "\n")
    print("Output Name: " + Output_Name + "\n")
    
    Project_Build_System = project_vars[4]
    # init dotnet
    await execute_code("csc " + Project_name + "/" + Entry_point, websocket)
    #output the exe to the build directory given the output name
    await execute_code("mv " + Output_Name + ".exe " + Project_name + "/" + Output_Name+".exe", websocket)
    # run the output
    await execute_code("mono " + Project_name + "/" + Output_Name + ".exe", websocket)
# init go
async def init_go(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]  
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    if _debug_enabled:
        print("Project Name: " + Project_name + "\n")
        print("Entry Point: " + Entry_point + "\n")
        print("Output Name: " + Output_Name + "\n")
    
    Project_Build_System = project_vars[4]
    # init go
    await execute_code("go run " + Project_name + "/" + Entry_point, websocket)

# init cmake
async def init_cmake(project_vars,websocket):
    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]  
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    if _debug_enabled:
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
    if _debug_enabled:
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

# init make
async def init_make(project_vars,websocket):

    # get the project vars
    Sysver = project_vars[0]
    Project_name = project_vars[1]
    Entry_point = project_vars[2]
    Output_Name = project_vars[3]
    if _debug_enabled:
        print("Project Name: " + Project_name + "\n")
        print("Entry Point: " + Entry_point + "\n")
        print("Output Name: " + Output_Name + "\n")
    Project_Build_System = project_vars[4]
    args = project_vars[5]
    # run make    
    if args: # if it's not empty then we can run make with the args that might point to a different makefile command
        await execute_code("make -C " + Project_name + " " + args, websocket)
        print("Running make with args")
        print("make -c " + Project_name + " " + args)
    else:
        await execute_code("make -C " + Project_name, websocket)
    # run the output
    await execute_code("./" + Project_name + "/" + Output_Name, websocket)
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
            await init_make(project_vars,websocket)
        case "g++":
            await init_gpp(project_vars,websocket)
        case "java":
            await execute_code("javac " + Project_name + "/" + Entry_point, websocket)
            await execute_code("java " + Project_name + "/" + Entry_point, websocket)
        case "maven":
            pass
        case "node":
            await init_node(project_vars,websocket)
        case "yarn":    
            pass    
        case "Python":
            await execute_code("python3 " + Project_name + "/" + Entry_point, websocket)
        case "cargo":
            pass
        case "rustc":
            await execute_code("rustc " + Project_name + "/" + Entry_point + " -o " + Project_name + "/" + Output_Name, websocket)
            await execute_code("./" + Project_name + "/" + Output_Name, websocket)
        case "Go":
            await init_go(project_vars,websocket)
        case "mono":
            await init_mono(project_vars,websocket)
        case "bash":
            await execute_code("bash " + Project_name + "/" + Entry_point, websocket)
        case "perl":
            await execute_code("perl " + Project_name + "/" + Entry_point, websocket)
        case "php":
            await execute_code("php " + Project_name + "/" + Entry_point, websocket)
        case "ruby":
            await execute_code("ruby " + Project_name + "/" + Entry_point, websocket)
        case "lua":
            await execute_code("lua " + Project_name + "/" + Entry_point, websocket)
    

            
async def PMS(websocket, path):
    # main function for the PMS system
    if _debug_enabled:
        print("PMS System")
        print("Path: " + path)
        print("Websocket: " + str(websocket))


    code = await websocket.recv()
    parsed_code = json.loads(code)
    print("Code: " + str(parsed_code))
    await Read_PMS_File(websocket,path, code)
        