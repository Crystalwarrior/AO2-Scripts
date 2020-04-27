import os
import sys
import yaml

dirpath = os.path.dirname(__file__)
os.chdir(dirpath)

arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]

musiclist = None
if arg != "":
    with open(arg, 'r', encoding='utf-8') as music:
        musiclist = yaml.load(music)

File = open("music categorizer.bat", "w")
current_category = ""
if musiclist:
    input("Making a .bat file to recategorize music based on .yaml file. Press ENTER to begin.")
    File.write('CD base\n')
    File.write('CD sounds\n')
    File.write('CD music\n')
    for item in musiclist:
        if 'category' not in item:
            continue
        cat = item['category'].strip('=')
        File.write('IF NOT EXIST "{}" MKDIR "{}"\n'.format(cat, cat))
        for song in item['songs']:
            File.write('MOVE "{}" "{}"\n'.format(song['name'], os.path.join(cat, song['name'])))
    input("Done! Press ENTER to exit.")
else:
    input("You must drag a music.yaml on top of this script to begin.")
