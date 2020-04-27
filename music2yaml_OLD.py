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

File = open("music.yaml", "w")
Err = open("music_errors.txt", "w")
if droppedFile:
    input("Writing .ogg and .mp3 and categorizing them based on file argument to music.yaml. Press ENTER to begin.")
    for line in droppedFile.readlines():
        try:
            line = line.rstrip()
            if line.lower().startswith('[mod]'):
                continue
            if line.lower().endswith(':'):
                File.write('- category: =={}==\n'.format(line[:-1]))
                File.write('  songs:\n')
                print("Category: {}".format(line[:-1]))
            if line.lower().endswith(('.mp3', '.ogg')):
                try:
                    tag = TinyTag.get(line)
                    File.write('    - name: "{}"\n'.format(line))
                    File.write('      length: {}\n'.format(tag.duration))
                    print("Name: {} Length: {}".format(line, tag.duration))
                except:
                    Err.write('Error for {}\n'.format(line))
                    input("Unable to process song: {}! Press ENTER to continue.".format(line))
        except:
            continue
else:
    input("Writing all .ogg and .mp3 present in folder to music.yaml. Any subfolders will be made as new categories. Press ENTER to begin.")

    for f in os.scandir(os.getcwd()):
        # if f.is_file():
        #     if f.name.endswith(('.mp3', '.ogg')):
        #         print('Music: ' + f.name)
        if f.is_dir():
            print('Folder: ' + f.path)
            File.write('- category: =={}==\n'.format(f.name))
            File.write('  songs:\n')
            for song in os.scandir(f.path):
                if song.is_file():
                    print(song)
                    if song.name.lower().startswith('[mod]'):
                        continue
                    if song.name.lower().endswith(('.mp3', '.ogg')):
                        tag = TinyTag.get(song.path)
                        File.write('    - name: "{}"\n'.format(song.name))
                        File.write('      length: {}\n'.format(tag.duration))
                        print("Name: {} Length: {}".format(song.name, tag.duration))

                        Dir = os.path.join(os.getcwd(), '_export')
                        if not os.path.exists(Dir):
                            os.makedirs(Dir)
                        copy2(song.path, '{}/{}'.format(Dir, song.name))
                        print('{}/{}'.format(Dir, song.name))
            
# else:
#     input("Writing all .ogg and .mp3 present in folder to music.yaml. Press ENTER to begin.")
#     File.write('- category: --IMPORT--\n')
#     File.write('  songs:\n')
#     for song in os.listdir():
#         try:
#             print(song)
#             if song.lower().startswith('[mod]'):
#                 continue
#             if song.lower().endswith(('.mp3', '.ogg')):
#                 tag = TinyTag.get(song)
#                 File.write('    - name: "{}"\n'.format(song))
#                 File.write('      length: {}\n'.format(tag.duration))
#                 print("Name: {} Length: {}".format(song, tag.duration))
#         except:
#             continue

input("Done! Press ENTER to exit.")
