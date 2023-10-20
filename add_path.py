import os
import sys
import time

from win10toast import ToastNotifier


def wait():
    while toaster.notification_active():
        time.sleep(0.1)
    return


toaster = ToastNotifier()
# # Example
# # toaster.show_toast(
# #     "Hello World!!!",
# #     "Python is 10 seconds awsm!",
# #     duration=10)
# toaster.show_toast(
#     "Example two",
#     "This notification is in it's own thread!",
#     icon_path=None,
#     duration=5,
#     threaded=True
# )
# # Wait for threaded notification to finish
# while toaster.notification_active():
#     time.sleep(0.1)

path_list = sys.argv[1:]
path_list_str = "\n".join(path_list)
toaster.show_toast(f"args: {path_list}", f"{path_list_str}")
wait()
for path in path_list:
    if os.path.exists(path) and os.path.isdir(path):
        with open(r".\data\targets.txt", "r") as f:
            target_folders = f.readlines()
            flag = False
            for target_folder in target_folders:
                if os.path.abspath(target_folder) == os.path.abspath(path):
                    print("Already exists")
                    flag = True
                    break
            if flag:
                toaster.show_toast("Invalid path", f.read())
                wait()
            else:
                with open(r".\data\targets.txt", "a") as f:
                    f.write("\n"+path + "\n")
                toaster.show_toast("Added", path)
                wait()
    else:
        toaster.show_toast("Invalid path", path)
        wait()
