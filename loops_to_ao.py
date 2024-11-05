import os
import sys

arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]

scandir = os.getcwd()

droppedFile = None
if arg != "":
    if os.path.isfile(arg):
        droppedFile = open(arg, "r")
    elif os.path.isdir(arg):
        scandir = arg

if not droppedFile:
    print("No file provided. Searching for 'LooperOutput' folder with 'loops.txt' file...")
    looper_output = f'{scandir}\\LooperOutput'
    if os.path.isdir(looper_output):
        loops_txt = f'{looper_output}\\loops.txt'
        if os.path.isfile(loops_txt):
            droppedFile = open(loops_txt, "r")
            print("Success!")

if not droppedFile:
    print("No loops.txt file found! Can't convert loops to AO format.")
else:
    for line in droppedFile.readlines():
        args = line.split(' ', 2)
        loop_start = args[0]
        loop_end = args[1]
        filename = args[2].strip()
        filestring = f'loop_start={loop_start}\nloop_end={loop_end}'
        print(f'Writing to {filename}.txt:\n{filestring}\n----')
        
        File = open(f'{filename}.txt', "w")
        File.write(filestring)
input("Press any key to continue... ")