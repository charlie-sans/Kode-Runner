def translate_terminal_colors(code):
    color_mapping = {
        '0': 'gray',
        '1': 'red',
        '2': 'green',
        '3': 'yellow',
        '4': 'blue',
        '5': 'magenta',
        '6': 'cyan',
        '7': 'white',
        '9': 'red',
        '10': 'green',
        '11': 'yellow',
        '12': 'blue',
        '13': 'magenta',
        '14': 'cyan',
        '15': 'white',
        '9': 'red',
        '10': 'green',
        '11': 'yellow',
        '12': 'blue',
        '13': 'magenta',
        '14': 'cyan',
        '15': 'white',
        '[51C': 'red',
        '[21a': '',
        '[K': '',
        '31': 'red',
        '32': 'green',
        '33': 'yellow',
        '34': 'blue',
        '35': 'magenta',
        '36': 'cyan',
        '37': 'white',
  
        '101': 'red',
        '110': 'green',
        '111': 'yellow',
        '112': 'blue',
        '113': 'magenta',
        '114': 'cyan',
        '115': 'white',
        
        '41': 'red',
        '42': 'green',
        '43': 'yellow',
        '44': 'blue',
        '45': 'magenta',
        '46': 'cyan',
        '47': 'white',
   
        '101': 'red',
        '102': 'green',
        '103': 'yellow',
        '104': 'blue',
        '105': 'magenta',
        '106': 'cyan',
        '107': 'white'
    }
    
    translated_code = ''
    i = 0
    while i < len(code):
        if code[i] == '\x1b' and code[i+1] == '[':
            j = i + 2
            while code[j].isdigit() or code[j] == ';':
                j += 1
            if code[j] == 'm':
                color_codes = code[i+2:j].split(';')
                for color_code in color_codes:
                    if color_code in color_mapping:
                        translated_code += f'<color={color_mapping[color_code]}>'
                    else:
                        translated_code += f'<color={color_code}>'
                i = j + 1
                continue
        translated_code += code[i]
        i += 1
    
    return translated_code


def translate_ansi_code(code):
    color_mapping = {
        '0': 'gray',
        '1': 'red',
        '2': 'green',
        '3': 'yellow',
        '4': 'blue',
        '5': 'magenta',
        '6': 'cyan',
        '7': 'white',
        '9': 'red',
        '10': 'green',
        '11': 'yellow',
        '12': 'blue',
        '13': 'magenta',
        '14': 'cyan',
        '15': 'white',
        '9': 'red',
        '10': 'green',
        '11': 'yellow',
        '12': 'blue',
        '13': 'magenta',
        '14': 'cyan',
        '15': 'white',
        '[51C': 'red',
        '[21a': '',
        '[K': '',
        '31': 'red',
        '32': 'green',
        '33': 'yellow',
        '34': 'blue',
        '35': 'magenta',
        '36': 'cyan',
        '37': 'white',
  
        '101': 'red',
        '110': 'green',
        '111': 'yellow',
        '112': 'blue',
        '113': 'magenta',
        '114': 'cyan',
        '115': 'white',
        
        '41': 'red',
        '42': 'green',
        '43': 'yellow',
        '44': 'blue',
        '45': 'magenta',
        '46': 'cyan',
        '47': 'white',
   
        '101': 'red',
        '102': 'green',
        '103': 'yellow',
        '104': 'blue',
        '105': 'magenta',
        '106': 'cyan',
        '107': 'white'
    }
    
    num = code[2:-1]
    if num in color_mapping:
        return(f'<color={color_mapping[num]}>')
    else:
        return(f'<color={num}>')


global line, ansi_code_stage, code_start

line = ""
# 0: not a ansi code
# 1: ESC code found
# 2: [ Found
# 3: m Found
ansi_code_stage = 0
code_start = -1

def new_char(char):
    global line, ansi_code_stage, code_start
    send_char = True
    
    if ansi_code_stage == 0 and char == "\x1b":
        code_start = len(line)
        ansi_code_stage = 1
        send_char = False
    elif ansi_code_stage == 1 and char == "[":
        ansi_code_stage = 2
        send_char = False
    elif ansi_code_stage == 2 and char == "m":
        ansi_code_stage = 3
        send_char = False
    elif char not in "0123456789" or ansi_code_stage != 2: # reset if invalid code
        ansi_code_stage = 0
        print(line[-code_start:])
        
    if ansi_code_stage == 3:
        ansi_code = line[-code_start:]
        
        ansi_code_stage = 0 # reset
        line = ""
        
        return translate_ansi_code(ansi_code) # return translated code.
    
    if char == "\n":
        line = ""

    line+=char
    if send_char:
        return char
    