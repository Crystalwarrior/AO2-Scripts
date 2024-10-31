import os
import sys
import configparser

arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]

droppedFile = None
if arg != "":
    droppedFile = open(arg, "r")

if not droppedFile:
    print("ERROR: DRO music ini file not provided!")
    raise

# change dirname to the found file
os.chdir(os.path.dirname(arg))

config = configparser.ConfigParser()
config.read(arg)
for section in config.sections():
    song_data = ""
    song_path = ""
    for key in config[section]:
        value = config[section][key]
        # not sure if "loop_length" is a thing for dro inis but including just to be safe
        if key == 'loop_start' or key == 'loop_length' or key == 'loop_end':
            song_data += f'{key}={value}\n'
        if key == 'filename':
            # Remove the first and last characters from the string, which should be ""
            song_path = value[1:][:-1]
    if song_path and song_data:
        File = open(f'{song_path}.txt', "w")
        File.write(song_data)
        print(f"Creating {song_path}.txt with data:\n{song_data}----\n")

input("Done! (Press any key to exit.)")