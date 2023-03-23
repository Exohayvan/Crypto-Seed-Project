import sys
import os
import platform

os_type = sys.platform
os.system('nuitka3 --follow-imports --output-dir=output_folder your_file_name.py')
