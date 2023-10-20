import os

# os.system(r'start "" ".\python\python.exe" add_path.py')
os.system(rf'".\python\python.exe" add_path.py {" ".join(input("args: ").split())}')
