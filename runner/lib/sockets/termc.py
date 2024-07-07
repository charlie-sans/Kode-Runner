import re

def convert_16bit_to_rgb(bit16):
    red = ((bit16 >> 11) & 0x1F) * 255 // 31
    green = ((bit16 >> 5) & 0x3F) * 255 // 63
    blue = (bit16 & 0x1F) * 255 // 31
    return red, green, blue

def rgb_to_hex(red, green, blue):
    return f"#{red:02x}{green:02x}{blue:02x}"

def convert_string_to_color_code(input_string):
    pattern = r"(?:\x1b\[)?(\d+)m(.*?)"
    result_string = input_string

    for match in re.finditer(pattern, input_string):
        color_code = match.group(1)
        text = match.group(2)

        if color_code.isdigit():
            bit16 = int(color_code)
            red, green, blue = convert_16bit_to_rgb(bit16)
        else:
            # Handle ANSI escape codes here
            ansi_code = color_code
            if ansi_code == "31":  # Red
                red, green, blue = 255, 0, 0
            elif ansi_code == "32":  # Green
                red, green, blue = 0, 255, 0
            elif ansi_code == "34":  # Blue
                red, green, blue = 0, 0, 255
            else:
                # If the color code is not found, you can choose a default color
                red, green, blue = 0, 0, 0

        hex_color = rgb_to_hex(red, green, blue)
        result_string = result_string.replace(match.group(0), f"<color={hex_color}>{text}</color>")

    return result_string
if __name__ == "__main__":
    # Test the function
    input_string = "\x1b[31mHello, \x1b[32mWorld!\x1b[0m"
    output_string = convert_string_to_color_code(input_string)
    print(output_string)  # <color=#ff0000>Hello, </color><color=#00ff00>World!</color>
