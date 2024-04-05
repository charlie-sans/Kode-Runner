import ast
import os

def check_code_safety(code):
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
    def UnsafeCodeException(self):
        return self.message
    