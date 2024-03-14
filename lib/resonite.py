import subprocess
import os
import sys
import time
import threading
import random
import urllib.request
import urllib.parse
import json

def write(code, name):
  with open(name,"w") as f:
    f.write(code)
    
def wnr(code,name,command,command2): # write and run the file
  with open(name,"w" )as f:
    f.write(code)
  subprocess.call(command)
  subprocess.call(command2)
  
def rn(command): # run the command in the terminal
  subprocess.call(command)
  
def rn2(command,command2): # run the command in the terminal
  subprocess.call(command)
  subprocess.call(command2)
  
def rn3(command,command2,command3): # run the command in the terminal
  subprocess.call(command)
  subprocess.call(command2)
  subprocess.call(command3)
def rn4(command,command2,command3,command4): # run the command in the terminal
    subprocess.call(command)
    subprocess.call(command2)
    subprocess.call(command3)
    subprocess.call(command4) 
  
def get_host_time():
  return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def get_host_name():
  return os.uname()[1]

def get_host_user():
  return os.getlogin()

def mono(path,code):# mono software runner
  write(path,code)
  os.system("csc" +  " " + path)
  # get the name of the file without the extension
  name = os.path.splitext(path)[0]
  os.system(f"mono {name}")

