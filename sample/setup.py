import cx_Freeze
from cx_Freeze import *
import sys
if sys.platform == "win32":
     base = "Win32GUI"

imodules=['tkinter'] #modules to include

emodules=[] ###modules to NOT include
            #(useful if a module is forcefully installed
            #even if you don't want that module)



build_exe_options={"packages":imodules,"excludes":emodules}

setup(
        name= "Application Name",
        options={"build_exe":build_exe_options},
        executables=[
        Executable(
                 "pytally.py", base=base,
                )
            ]
        )
