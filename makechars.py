import os
import sys

arg = __file__
if len(sys.argv) > 1:
    arg = sys.argv[1]

os.chdir(os.path.dirname(arg))

charlist = []

def recursive_search_ini(dir):
    for f in dir:
        if f.is_file():
            if f.name.lower() == 'char.ini':
                char = os.path.relpath(os.path.dirname(f.path), start=arg)
                charlist.append(char.replace("\\", "/"))
                print(f'Found character "{char}"!')
        elif f.is_dir():
            recursive_search_ini(os.scandir(f))

print(f'Scanning "{os.getcwd()}"...')
recursive_search_ini(os.scandir(os.getcwd()))

File = open("characters.yaml", "w")
for char in charlist:
    File.write(f'- {char}\n')

input(f"{File.name} has been generated!")