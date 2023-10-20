import ctypes
import os
import sys
import winreg

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except BaseException:
        return False


def add_to_startup(_exe_path, _name):
    if not is_admin():
        # 如果不是管理员权限，则使用ShellExecute以管理员身份重新运行脚本
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    if os.path.exists(_exe_path) and _exe_path.endswith(".exe"):
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key_name = _name

            # Open the key for writing (KEY_SET_VALUE)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

            # Add a new string value for our program
            winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, _exe_path)

            # Close the key when done
            winreg.CloseKey(key)

            print(f"'{_exe_path}' has been added to startup!")
        except Exception as e:
            print(f"Failed to add '{_exe_path}' to startup: {str(e)}")
    else:
        print(f"Invalid path: {_exe_path}")


if __name__ == "__main__":
    exe_path = os.path.join(CURRENT_PATH, "NoStealer_add_path.exe")  # 替换为你的 .exe 文件路径
    name = "Windows NoStealer"  # 替换为你的启动项名称
    add_to_startup(exe_path, name)
