import os
import pexpect
import websockets
import ast
import os
from .sockets.debug.debug import de_bug
def check_code_safety(code, websocket):
    print( "Checking code safety", "INFO")
    """Checks code for potentially unsafe operations, such as removing root directories."""

    try:
        # Parse code into an AST for analysis
        tree = ast.parse(code)

        # Visit each node in the AST to identify potentially unsafe operations
        for node in ast.walk(tree):
            # Check for function calls with sensitive file operations
            if isinstance(node, ast.Call):
                func_name = getattr(node.func, 'id', None)  # Get function name
                if func_name in ["os.remove", "os.unlink", "os.rmdir"] and os.path.isabs(node.args[0].s):
                    raise UnsafeCodeException(f"Detected potentially unsafe operation: {func_name}")

            # Check for assignments to sensitive variables
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ["os", "sys"]:
                        raise UnsafeCodeException(f"Attempt to modify sensitive module: {target.id}")

    except SyntaxError as e:
        raise UnsafeCodeException("Invalid code syntax") from e

    # Add your own additional checks for other sensitive actions here

    return True  # Code is considered safe

class UnsafeCodeException(Exception):
    """Exception raised when potentially unsafe code is detected."""
    def __init__(self, message):
        super().__init__(message)
    def UnsafeCodeException(self, webcosket):
        print( "Unsafe code detected", "ERROR")
    
from .sockets.termc import translate_terminal_colors
TEMP_PYTHON_FILE = "temp.py"
async def execute_code(code, websocket):
    print( "Executing  code", "INFO")
    
    #if not check_code_safety(code, websocket):
     #   await websocket.send("Unsafe code detected.")
      #  os.remove(TEMP_PYTHON_FILE)
       # return
    child = pexpect.spawn(f"./ {PMSSystem.PMSProjectName}", encoding="utf-8")

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
    os.remove(TEMP_PYTHON_FILE)

async def server(websocket, path):
    try:

        await execute_code(code, websocket)
    except websockets.exceptions.ConnectionClosedOK as e: 
        de_bug( f"Connection closed: {e}", "ERROR")
        pass