import os
import sys
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "C:\\ProgramData\\Anaconda3\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\ProgramData\\Anaconda3\\tcl\\tk8.6"
setup(
    name = "Template GUI",
    version = "0.1",
    options = {"build_exe": {"packages": ["numpy"]}},
    description = "Test 01",
    executables = [Executable("test3.py", base=None)])
