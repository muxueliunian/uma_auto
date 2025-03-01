import os 
import ctypes
import sys

def is_admin():
    """检查当前是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return run_as_admin()

def run_as_admin():
    """以管理员权限重新运行程序"""
    if sys.argv[0].endswith('.py'):  # 如果是直接运行的.py文件
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:])
    else:  # 如果是打包后的exe文件
        params = ' '.join(sys.argv)
    
    # 对路径和参数进行引号转义处理
    if ' ' in params:
        params = f'"{params}"'
    
    ctypes.windll.shell32.ShellExecuteW(
        None,  # 父窗口句柄
        "runas",  # 操作类型：提权运行
        sys.executable,  # 可执行文件路径
        params,  # 参数
        None,  # 工作目录
        1  # 窗口显示方式：SW_SHOWNORMAL
    )
    sys.exit()  # 退出当前非特权进程

