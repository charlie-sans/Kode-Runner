import json

# The provided JSON string
json_string = '''
{
    "PMS_System": "1.0",
    "Project_Name": "<Project Name>",
    "Project_Files": [{
            "File_Name": "main.cpp",
            "File_Extention": ".cpp"
        },
        {
            "File_Name": "test.pms",
            "File_Extention": ".pms"
        }
    ],
    "Project_Build_System": "Rust",
    "Project_Output": "main.exe",
    "Project_Use_Multiple_Build_Systems": false,
    "Project_Build_Systems": [{
        "Build_System_Name": "Rust",
        "Build_System_Arguments": [{
                "Argument_Type": "string",
                "Argument_Value": "cpp"
            },
            {
                "Argument_Type": "json",
                "Argument_Value1": "main.cpp",
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
'''

# Parse the JSON string
data = json.loads(json_string)

# Initialize a list for storing values
values = []

# Function to replace values with placeholders and collect the original values
def replace_with_placeholders(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                replace_with_placeholders(value)
            else:
                values.append(value)
                obj[key] = f"{{{len(values) - 1}}}"
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                replace_with_placeholders(item)
            else:
                values.append(item)
                obj[index] = f"{{{len(values) - 1}}}"

# Replace values in the data with placeholders
replace_with_placeholders(data)

# Convert the modified JSON back to a string
json_with_placeholders = json.dumps(data, indent=4)

# Print the JSON with placeholders and the list of values
print("JSON with Placeholders:")
print(json_with_placeholders)
print("\nValues:")
print(values)
