import os
import subprocess
with open("main.js","w") as file:
   file.write('console.log("hello world")') 
subprocess.call("node main.js")
