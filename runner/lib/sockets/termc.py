import re

def parse_ansi_escape_codes(text):
    result = []
    current_color = None
    for char in text:
        if char == '\x1b':
            # Start of an escape sequence
            count = 1
            while count > 0:
                char = text[text.index(char) + count]
                if char == '[':
                    count += 1
                elif char == 'm':
                    count -= 1
            # Extract the color code
            color_code = text[text.index(char):text.index('m')].strip()
            if color_code.startswith('38'):
                # This is a 256-color code
                color_number = int(color_code.split(';')[1])
                hex_color = '#{:02x}{:02x}{:02x}'.format(*divmod(color_number * 10 % 256, 256))
                current_color = hex_color
            else:
                # Reset color
                current_color = None
            result.append((current_color, text[text.index(char):]))
        else:
            result.append((current_color, char))
    return result