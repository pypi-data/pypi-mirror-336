import os
import clr
# 导入命名空间
from _DataFuncApplication import *
from _CsToYjk import *
def initialize_environment():
    """自动加载当前目录下的 DLL 并导入命名空间"""
    current_directory = os.getcwd()  # 获取当前目录
    dll_path_yapi = os.path.join(current_directory, "DLLs", "YAPIData.dll")
    dll_path_yjkapi = os.path.join(current_directory, "DLLs", "YJKAPI.dll")
    
    # 加载 DLL
    clr.AddReference(dll_path_yapi)
    clr.AddReference(dll_path_yjkapi)
    

    
    print("Environment initialized successfully.")
