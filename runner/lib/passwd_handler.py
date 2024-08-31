__password = ""
def set_password(passwd): 
    global __password
    __password = passwd

print("CARSONCODER FUCKED UP AND PUSHED UNSAFE CODE. dont run this verison. I mean you can but dont ###########################################################")
def get_password(): # DO NOT PUSH TO PRODUCTION
    return __password

def has_password():
    return __password != ""
