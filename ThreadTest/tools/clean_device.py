from pyboard_tools import pyboard_tools
import sys
import platform

my_windows_com_port = "COM8"
my_linux_com_port = '/dev/ttyUSB0'

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

pyb_tools.clean_device(".");

del pyb_tools