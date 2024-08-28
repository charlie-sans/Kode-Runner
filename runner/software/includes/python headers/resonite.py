import string
import subprocess
import os
import sys
import time
import threading
import random
import urllib.request
import urllib.parse
import json

###
# the official resonite library
# Created by: Charlie_san
# Version: 1.0.0
# this library is a collection of functions that are used to write code at a faster pace with vr controllers
###

def get_random_string(length):
  """get random string

  Args:
      length (int): length of the string

  Returns:
      string: random string
  """
  letters = string.ascii_lowercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str

def get_random_number(length):
  """get random number

  Args:
      length (int): length of the number

  Returns:
      string: random number
  """
  letters = string.digits
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str
  
def get_random_string_and_number(length):
  """get random string and number


  Args:
      length (int): length of the string and number

  Returns:
      string: random string and number
  """
  letters = string.ascii_lowercase + string.digits
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str
  
def get_string_num_symbol(length): # get random string and number and symbols
  """get random string and number and symbols


  Args:
      length (int): length of the string and number and symbols


  Returns:
      string: random string and number and symbols
  """
  letters = string.ascii_lowercase + string.digits + string.punctuation
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str
  
def get_random_str_num_symbol_uppercase(length): # get random string and number and symbols and upper case 
  """get random string and number and symbols and upper case


  Args:
      length (int): length of the string and number and symbols and upper case


  Returns:
      string: random string and number and symbols and upper case
  """
  letters = string.ascii_lowercase + string.digits + string.punctuation + string.ascii_uppercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str

# logger wrapper
def logger(func):
  """logger wrapper


  Args:
      func (function): function to be wrapped


  Returns:
      function: wrapped function
  """
  def inner(*args, **kwargs):
    print(f"Function {func.__name__} has been called with args: {args} and kwargs: {kwargs}")
    return func(*args, **kwargs)
  return inner

# warning function
def warning(warning):
  """warning function


  Args:
      warning (string): warning message
  """
  print(f"[WARNING] {warning}")
  
# error function
def error(error):
  """error function


  Args:
      error (string): error message
  """
  print(f"[ERROR] {error}")
  
# info function
def info(info):
  """info function


  Args:
      info (string): info message
  """
  print(f"[INFO] {info}")
  
# debug function
def debug(debug):
  """"debug function


  Args:
      debug (string): debug message
  """  
  print(f"[DEBUG] {debug}")
  


def write(code, name):
  """write function


  Args:
      code (string): code to be written
      name (string): name of the file
  """
  with open(name,"w") as f:
    f.write(code)
    
def wnr(code,name,command,command2): # write and run the file
  """write and run the file


  Args:
      code (string): code to be written
      name (string): name of the file
      command (string): command to be run
      command2 (string): command to be run
  """
  with open(name,"w" )as f:
    f.write(code)
  os.system(command)
  os.system(command2)
  
def rn(command): 
  """run command


  Args:
      command (string): command to be run
"""
 
  os.system(command)

def rn2(command,command2): 
  """run command


  Args:
      command (string): first command to run
      command2 (string): seccond command to run
  """
  os.system(command)
  os.system(command2)

def rn3(command,command2,command3): 
  """run command


  Args:
      command (string): first command to run
      command2 (string): seccond command to run
      command3 (string): third command to run
  """
  os.system(command)
  os.system(command2)
  os.system(command3)

  
def get_host_time():
  """get host time



  Returns:
      string: host time
  """
  return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def get_host_name():
  """get host name



  Returns:
      string: host name
  """
  return os.uname()[1]

def get_host_user():
  return os.getlogin()

def mono(path,code):# mono software runner
  """mono software runner


  Args:
      path (string): the destination path
      code (string): the code to be written
  """
  write(path,code)
  os.system("csc" +  " " + path)
  # get the name of the file without the extension
  name = os.path.splitext(path)[0]
  os.system(f"mono {name}")