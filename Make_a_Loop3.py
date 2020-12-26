import os
import sys

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def makeLoopFile(arg):
    if arg.rsplit(".",1)[1] != "loop": # Check if the file end with .loop
        return
    f = open(arg, "rb") # File being Opened
    NewName = arg.rsplit(".",1)[0] + ".ogg.txt" # This is for naming the .ogg.txt later


    # These will find the relevant bytes in the .loop
    f.seek(4,0)
    Start = f.read(3)
    f.seek(8,0)
    End = f.read(3)

    # These are converting the Little Endians into Decimal
    LoopStart = int(Start[::-1].hex(), 16)
    LoopEnd = int(End[::-1].hex(), 16)

    # This is writing the AO2 Loop File
    New = open(NewName, "w+")
    New.write("loop_start = {} \nloop_end = {}".format(LoopStart, LoopEnd))

for file in os.listdir(os.getcwd()):
    makeLoopFile(file)