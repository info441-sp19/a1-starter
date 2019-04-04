import sys
import os
import subprocess

# change to python3 as needed
p = "python"

os.chdir("program_1/")

try:
    output = subprocess.check_output([p, "test.py"], text=True)
    print(output)
except:
    print("Failed to run Program 1")

os.chdir("../program_2/")

try:
    output = subprocess.check_output([p, "test.py"], text=True)
    print(output)
except:
    print("Failed to run Program 2")