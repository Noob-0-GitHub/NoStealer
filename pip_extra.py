import os


def install():
    while True:
        libs = input("install libs >> ")
        if libs.lower() in ["break", "b"]:
            break
        libs = libs.split()
        for lib in libs:
            os.system(fr'".\python\python.exe" -m pip install {lib}')


def pip():
    while True:
        command = input("pip >> ")
        if command.lower() in ["break", "b"]:
            break
        elif command.lower() in ["install", "i"]:
            install()
        else:
            os.system(fr'".\python\python.exe" -m pip {command}')


if __name__ == '__main__':
    pip()
