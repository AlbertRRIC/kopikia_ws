import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/jetsonros2/MyProject/kopikia_ws/install/kopikia_bot'
