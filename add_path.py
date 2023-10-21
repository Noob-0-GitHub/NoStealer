import os
import sys
import time

import win10toast

target_folders_file = os.path.abspath(r".\data\targets.txt")
if not os.path.exists(os.path.split(target_folders_file)[0]):
    os.makedirs(os.path.split(target_folders_file)[0], exist_ok=True)
if not os.path.exists(target_folders_file):
    with open(target_folders_file, "w") as f:
        f.write("")


class ToastNotifier(win10toast.ToastNotifier):
    def __init__(self):
        super().__init__()

    def on_destroy(self, hwnd, msg, wparam, lparam):
        super().on_destroy(hwnd, msg, wparam, lparam)
        return 0


def wait():
    while toaster.notification_active():
        time.sleep(0.1)
    return


toaster = ToastNotifier()

path_list = sys.argv[1:]
toaster.show_toast(f"args: {';'.join(path_list)}", "\n".join(path_list))
wait()
for path in path_list:
    if os.path.exists(path) and os.path.isdir(path):
        with open(target_folders_file, "r") as f:
            target_folders = f.read().split("\n")
            existed = False
            for target_folder in target_folders:
                if os.path.abspath(target_folder) == os.path.abspath(path):
                    toaster.show_toast("Already exists", path)
                    existed = True
                    break
        if existed:
            toaster.show_toast("Invalid path", f.read())
            wait()
        else:
            with open(target_folders_file, "a") as f:
                f.write("\n" + path + "\n")
            toaster.show_toast("Added", path)
            wait()
    else:
        toaster.show_toast("Invalid path", path)
        wait()
