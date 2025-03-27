import sys
import os

#獲取上一層路徑  如果是exe則返回當前exe所在的文件夾的名字
def get_out_dir(count:int) -> str:
    if is_executable():
        current_path = os.path.dirname(sys.executable)  #exe所在的文件夾的名字
        return current_path
    else:
        # 获取当前脚本文件的路径
        current_path = os.path.abspath(__file__)
        # 逐级向上获取父目录路径
        for _ in range(count):
            current_path = os.path.dirname(current_path)
        return current_path

def is_executable() -> bool:
    return not sys.executable.endswith('python.exe')

def is_dir_exists(path: str) -> bool:
    return os.path.isdir(path)

def is_file_exists(path: str) -> bool:
    return os.path.isfile(path)
