import os
import binascii

file_path = 'c++.7zbson'

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File {file_path} does not exist.")
else:
    try:
        with open(file_path, 'rb') as f:
            byte_data = f.read()

        # Convert bytes to hexadecimal and print
        hex_data = binascii.hexlify(byte_data)
        print(hex_data)
    except Exception as e:
        print(f"Failed to read file {file_path}: {e}")