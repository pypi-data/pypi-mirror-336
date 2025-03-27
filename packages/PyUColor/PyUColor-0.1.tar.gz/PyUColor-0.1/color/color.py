"""
  #####   #####   #       #####   #####  
  #       #   #   #       #   #   #   #   
  #       #   #   #       #   #   #####  
  #       #   #   #       #   #   #  #
  #####   #####   #####   #####   #   #    
  By @urielmalka

  The Color Print Library is a C language utility that allows for colored text output in terminal applications. 
  It provides functions for printing text in various colors and styles, including bold, italic, and underlined text.

  Check my GitHub: https://github.com/urielmalka

"""


import ctypes
from enum import Enum
import platform
import os

class Color(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5 
    CYAN = 6

# Load the shared library

if platform.system() == 'Windows':
    lib_path = os.path.join(os.path.dirname(__file__), 'print-color.dll')
    lib = ctypes.CDLL(lib_path)
else:
    lib_path = os.path.join(os.path.dirname(__file__), 'libprint-color.so')
    lib = ctypes.CDLL(lib_path)

# Define the argument types
lib.printc.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.printcb.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.printci.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.printcu.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.printcd.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.printcm.argtypes = [ctypes.c_int, ctypes.c_char_p]

def printc(color_code, message,end="\n"):
    lib.printc(color_code, f"{message}{end}".encode('utf-8'))

def printcb(color_code, message, end="\n"):
    lib.printcb(color_code, f"{message}{end}".encode('utf-8'))

def printci(color_code, message, end="\n"):
    lib.printci(color_code, f"{message}{end}".encode('utf-8'))

def printcu(color_code, message, end="\n"):
    lib.printcu(color_code, f"{message}{end}".encode('utf-8'))

def printcd(color_code, message, end="\n"):
    lib.printcd(color_code, f"{message}{end}".encode('utf-8'))

def printcm(color_code, message, end="\n"):
    lib.printcm(color_code, f"{message}{end}".encode('utf-8'))


printc(1,"hhee")