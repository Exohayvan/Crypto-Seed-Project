import sys
import os
import platform
os_type = sys.platform
os.system('pyinstaller --onefile main.py')
