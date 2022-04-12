from tinytag import TinyTag
import os
import sys

from shutil import copy2

os.chdir(os.path.dirname(__file__))

arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]

droppedFile = None
if arg != "":
    droppedFile = open(arg, "r")

use_lengths = input(
    'Analyze song lengths and put them in length:? (y/n)').lower() == 'y'

File = open("music.yaml", "w")
Err = open("music_errors.txt", "w")
current_category = ""
File.write('- replace: False #Whether or not to use this music list exclusively instead of trying to add it on top of server music\n')
File.write('  use_unique_folder: True #If true, this music will be contained entirely within its own folder e.g. base/music/<yaml name>/*.mp3\n')
if droppedFile:
    input("Writing .mp3, .ogg, .opus, .wav and .m4a and categorizing them based on file argument to music.yaml. Press ENTER to begin.")
    for line in droppedFile.readlines():
        try:
            line = line.rstrip()
            if line.lower().startswith('[mod]'):
                continue
            if line.lower().endswith(('.mp3', '.ogg', '.opus', '.wav', '.m4a')):
                try:
                    if line.lower().endswith(':') and current_category != line[:-1]:
                        File.write('- category: =={}==\n'.format(line[:-1]))
                        File.write('  songs:\n')
                        print("Category: {}".format(line[:-1]))
                        current_category = line[:-1]
                    duration = -1
                    if use_lengths:
                        tag = TinyTag.get(line)
                        duration = tag.duration
                    File.write(
                        '    - name: "{}"\n'.format(current_category + "/" + line))
                    File.write('      length: {}\n'.format(duration))
                    print("Name: {} Length: {}".format(line, duration))
                except:
                    Err.write('Error for {}\n'.format(line))
                    input(
                        "Unable to process song: {}! Press ENTER to continue.".format(line))
        except:
            continue
else:
    input("Writing all .mp3, .ogg, .opus, .wav and .m4a present in current folder/subfolders to music.yaml. Any subfolders will be made as new categories. Press ENTER to begin.")

    for f in os.scandir(os.getcwd()):
        if f.is_file():
            if f.name.lower().startswith('[mod]'):
                continue
            if f.name.lower().endswith(('.mp3', '.ogg', '.opus', '.wav', '.m4a')):
                if current_category != 'Unsorted':
                    current_category = 'Unsorted'
                    File.write('- category: ==Unsorted==\n')
                    File.write('  songs:\n')
                duration = -1
                File.write('    - name: "{}"\n'.format(f.name))
                File.write('      length: {}\n'.format(duration))
                print("Name: {} Length: {}".format(f.name, duration))
        elif f.is_dir():
            print('Folder: ' + f.path)
            for song in os.scandir(f.path):
                if song.is_file():
                    print(song)
                    if song.name.lower().startswith('[mod]'):
                        continue
                    if song.name.lower().endswith(('.mp3', '.ogg', '.opus', '.wav', '.m4a')):
                        if current_category != f.name:
                            current_category = f.name
                            File.write('- category: =={}==\n'.format(f.name))
                            File.write('  songs:\n')
                        duration = -1
                        if use_lengths:
                            tag = TinyTag.get(song.name)
                            duration = tag.duration
                        File.write(
                            '    - name: "{}"\n'.format(current_category + "/" + song.name))
                        File.write('      length: {}\n'.format(duration))
                        print("Name: {} Length: {}".format(song.name, duration))

                        # Dir = os.path.join(os.getcwd(), '_export')
                        # if not os.path.exists(Dir):
                        #     os.makedirs(Dir)
                        # copy2(song.path, '{}/{}'.format(Dir, song.name))
                        # print('{}/{}'.format(Dir, song.name))

input("Done! Press ENTER to exit.")
