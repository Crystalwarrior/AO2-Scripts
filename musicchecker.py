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

Err = open("music_missing.txt", "w", encoding='utf-8')
Err2 = open("music_extra.txt", "w", encoding='utf-8')
if musiclist:
    musics = []
    for item in musiclist:
        for song in item['songs']:
            musics.append(song['name'])

    for song in musics:
        if not (song in songs):
            Err.write('{}\n'.format(song))
            print("Song {} missing!".format(song))

    input("Checked for songs missing from music.yaml that should've been there. Press ENTER to check for songs that shouldn't be there.")

    for song in songs:
        if not (song in musics):
            Err2.write('{}\n'.format(song))
            print("Song {} is extra!".format(song))
    input("Done!")
else:
    input("Usage: drag and drop music.yaml on this program to check if any of the songs are missing from it.")
