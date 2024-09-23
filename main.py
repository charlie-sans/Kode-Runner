import os
import ast
import json

def infer_type(value):
    """Infer the type of a value."""
    if isinstance(value, ast.Constant):
        return type(value.value).__name__
    elif isinstance(value, ast.List):
        return "list"
    elif isinstance(value, ast.Dict):
        return "dict"
    elif isinstance(value, ast.Tuple):
        return "tuple"
    elif isinstance(value, ast.Set):
        return "set"
    elif isinstance(value, ast.Call):
        return value.func.id if isinstance(value.func, ast.Name) else None
    return None

def parse_function_def(node):
    """Parse a function definition node to extract relevant information."""
    func_info = {
        "name": node.name,
        "args": [],
        "description": ast.get_docstring(node) or "",
        "return": None,
        "async": isinstance(node, ast.AsyncFunctionDef)
    }

    for arg in node.args.args:
        arg_info = {
            "name": arg.arg,
            "type": None,
            "default": None
        }
        if arg.annotation:
            arg_info["type"] = ast.unparse(arg.annotation) if hasattr(ast, 'unparse') else ast.dump(arg.annotation)
        func_info["args"].append(arg_info)

    if node.returns:
        func_info["return"] = ast.unparse(node.returns) if hasattr(ast, 'unparse') else ast.dump(node.returns)

    return func_info

def parse_variable_assignments(node, func_name=None):
    """Parse variable assignments to extract relevant information."""
    variables = []
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_info = {
                    "name": target.id,
                    "value": ast.unparse(node.value) if hasattr(ast, 'unparse') else ast.dump(node.value),
                    "type": infer_type(node.value),
                    "function": func_name
                }
                variables.append(var_info)
    return variables

def parse_python_file(file_path):
    """Parse a Python file to extract function definitions and variable assignments."""
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)

    functions = []
    variables = []
    docstring = ast.get_docstring(tree) or ""

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(parse_function_def(node))
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Assign):
                    variables.extend(parse_variable_assignments(sub_node, node.name))
        elif isinstance(node, ast.Assign):
            variables.extend(parse_variable_assignments(node))

    return {
        "docstring": docstring,
        "functions": functions,
        "variables": variables,
        "function_count": len(functions),
        "variable_count": len(variables)
    }

def generate_json_for_directory(directory_path):
    """Generate JSON representation for all Python files in a directory."""
    total_functions = 0
    total_variables = 0
    all_files_info = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_info = parse_python_file(file_path)
                total_functions += file_info["function_count"]
                total_variables += file_info["variable_count"]
                all_files_info.append({
                    "file_path": file_path,
                    "docstring": file_info["docstring"],
                    "functions": file_info["functions"],
                    "variables": file_info["variables"],
                    "function_count": file_info["function_count"],
                    "variable_count": file_info["variable_count"]
                })

    project_info = {
        "name": "Python",
        "description": "description for file",
        "total_function_count": total_functions,
        "total_variable_count": total_variables,
        "files": all_files_info
    }

    # write the contents to the json/ directory
    json_file_path = os.path.join("json", "project_info.json")
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, "w") as json_file:
        json.dump(project_info, json_file, indent=4)
    print(f"Generated JSON for directory {directory_path}")

if __name__ == "__main__":
    directory_path = "runner/"
    generate_json_for_directory(directory_path)
