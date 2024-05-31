from pyboard_tools import pyboard_tools
import sys
import platform
from pyboard_tools import pyboard_tools
import sys


my_windows_com_port = "COM8" # Windows port definition
my_linux_com_port = '/dev/ttyUSB0' # Linux port definition

arg_len = len(sys.argv)
if arg_len < 2:
    platform = platform.system()
    if platform == 'Windows':
        com_port = my_windows_com_port
    elif platform == 'Linux':
        com_port = my_linux_com_port
    else:
        print("Unkown OS platform")
        exit()

pyb_tools = pyboard_tools(com_port)

pyb_tools.upload_files_to_device("../device", ".")

del pyb_tools