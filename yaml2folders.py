from tinytag import TinyTag
import os
import sys

import yaml

from shutil import copy2

os.chdir(os.path.dirname(__file__))

arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]

musiclist = None
if arg != "":
    with open(arg, 'r', encoding='utf-8') as music:
        musiclist = yaml.load(music)

songs = list(filter(lambda x: os.path.isfile(x) and x.lower().endswith(('.mp3', '.ogg')), os.listdir(os.getcwd())))

Log = open("music_log.txt", "w", encoding='utf-8')
if musiclist:
    musics = []
    for item in musiclist:
        if 'category' not in item:
            continue
        cat = item['category'].strip('=')
        Dir = os.path.join(os.getcwd(), cat)
        if not os.path.exists(Dir):
            os.makedirs(Dir)
        for song in item['songs']:
            try:
                song['name'] = song['name'][song['name'].find('/')+1:]
                F = os.path.join(os.getcwd(), song['name'])
                copy2(F, '{}/'.format(Dir))
                print('{}/{}'.format(cat, song['name']))
                Log.write('{}/{}\n'.format(cat, song['name']))
            except:
                Log.write('Song {} missing!\n'.format(song['name']))
                print("Song {} missing!".format(song['name']))
    input("Done!")
else:
    input("Usage: drag and drop music.yaml on this program to copy all songs to categories.")
