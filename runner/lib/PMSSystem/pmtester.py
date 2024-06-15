import asyncio
import os
import json as js

try:
    import websockets
except ImportError:
    print("Websockets not installed. Running 'pip install websockets' to install it")
    os.system("pip install websockets")
    import websockets
    
# PMSSystem tester


# open the websocket server

jsonz = """{
    "PMS_System": "1.0",
    "Project_Name": "Coderunner",
    "Project_Files": [{
            "File_Name": "main",
            "File_Extention": ".cpp"
            },
            {
            "File_Name": "imgui",
            "File_Extention": ".cpp"
            },
            {
            "File_Name": "imgui_demo",
            "File_Extention": ".cpp"
            },
            {
            "File_Name": "imgui_draw",
            "File_Extention": ".cpp"
            },
        {
            "File_Name": "test",
            "File_Extention": ".hpp"
            }
    ],
    "Project_Build_System": "Rust",
    "Project_Output": "main.exe",
    "Project_Use_Multiple_Build_Systems": false,
    "Project_Build_Systems": [{
        "Build_System_Name": "Rust",
        "Build_System_Arguments": [{
                "Argument_Type": "string",
                "Argument_Value": "c++"
            },
            {
                "Argument_Type": "json",
                "Argument_Value2": "test.pms"
            },
            {
                "Argument_Type": "string",
                "Argument_Value1": "main.exe"
            },
            {
                "Argument_Type": "bool",
                "Argument_Value1": false
            }
        ]
    }],
    "Project_Use_Language_Server_Protocol": false,
    "Project_Language_Server_Protocol": {
        "Language_Server_Protocol_Name": "LSP",
        "Language_Server_Protocol_Version": "1.0",
        "Language_Server_Protocol_Support": [{
                "Support_Type": "Code_Completion",
                "Support_Value": true
            },
            {
                "Support_Type": "Error_Checking",
                "Support_Value": true
            }
        ]
    },
    "Project_Error_Handling": {
        "Error_Handling_Type": "Client",
        "Error_Handling_Support": true
    },
    "Project_Code_Completion": {
        "Code_Completion_Type": "Client",
        "Code_Completion_Support": true
    },
    "Project_Multiple_Files_Support": {
        "Multiple_Files_Type": "Client",
        "Multiple_Files_Support": true
    },
    "Project_GUI": {
        "GUI_Type": "Client",
        "GUI_Style": [{
                "Style_Type": "Jetbrains",
                "Is_active": true
            },
            {
                "Style_Type": "Visual_Studio",
                "Is_active": false
            },
            {
                "Style_Type": "Visual_Studio_Code",
                "Is_active": false
            }
        ]
    }
}
"""

jzons = js.loads(jsonz)
# read the json array of files and the contents of the files

for project_file in jzons["Project_Files"]:
    # Extract and assign the values to variables
    file_name = project_file["File_Name"]
    file_extension = project_file["File_Extention"]
    print(f"File Name: {file_name}, File Extension: {file_extension}")