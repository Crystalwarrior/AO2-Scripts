import os

File = open("musiclist.txt", "w")

File.write('Music dump:\n')
for song in os.listdir():
    try:
        if song.lower().endswith(('.mp3', '.ogg')):
            File.write(song + '\n')
    except:
        continue
