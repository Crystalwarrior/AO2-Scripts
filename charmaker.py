import os
import shutil
import sys
import re


def natural_sort(l):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


directory = os.path.dirname(__file__)
os.chdir(directory)

File = open("char.ini", "w")

File.write('[Options]\n')
File.write('name = {}\n'.format(os.path.basename(directory)))
File.write('showname = {}\n'.format(input("Please input showname.")))
File.write('side = {}\n'.format('wit'))
File.write('gender = {}\n'.format(input("Please input gender.")))

folder_sort = input(
    'Sort all the emotes into "(a)" "(b)" "anim" folders? (y/n)').lower() == 'y'

input("Writing all images in folder to char.ini. Press ENTER to begin.")
emote_number = 0
string = ''
timestring = ''

idle_emotes = []
talking_emotes = []
pre_emotes = []
for emote in natural_sort(os.listdir()):
    try:
        if emote.lower() != "char_icon.png" and emote.lower().endswith(('.png', '.gif', '.webp', '.apng')):
            if emote.lower().startswith('(a)'):
                idle_emotes.append(emote)
            elif emote.lower().startswith('(b)'):
                talking_emotes.append(emote)
            else:
                pre_emotes.append(emote)
    except:
        continue

# Move the idle anims into their folders
for v, emote in enumerate(idle_emotes):
    filename = emote[3:]
    name = filename[:filename.rfind('.')]
    prefix = '(a)'
    if folder_sort:
        Dir = '{}/{}/'.format(directory, prefix)
        if not os.path.exists(Dir):
            os.makedirs(Dir)
        shutil.move('{}/{}'.format(directory, emote),
                    '{}/{}'.format(Dir, filename))
    print(f'{prefix} = {name}')

    # update the index
    if emote_number <= v:
        emote_number = v+1

# Move the talking anims into their folders
for emote in talking_emotes:
    filename = emote[3:]
    name = filename[:filename.rfind('.')]
    prefix = '(b)'
    if folder_sort:
        Dir = '{}/{}/'.format(directory, prefix)
        if not os.path.exists(Dir):
            os.makedirs(Dir)
        shutil.move('{}/{}'.format(directory, emote),
                    '{}/{}'.format(Dir, filename))
    print(f'{prefix} = {name}')

# Move the preanims into their own folders only if they have an associated idle
for v, emote in enumerate(pre_emotes):
    name = emote[:emote.rfind('.')]
    prefix = 'anim'
    if folder_sort:
        Dir = '{}/{}/'.format(directory, prefix)
        if not os.path.exists(Dir):
            os.makedirs(Dir)
        shutil.move('{}/{}'.format(directory, emote),
                    '{}/{}'.format(Dir, emote))
        pre_emotes[v] = f'{prefix}/{emote}'
    print(f'{prefix} = {name}')

    # update the index
    if emote_number <= v:
        emote_number = v+1

print(emote_number)
for idx in range(0, emote_number):
    pre = '-'
    idle = '-'
    if idx < len(idle_emotes):
        emote = idle_emotes[idx]
        if emote.lower().startswith('(a)'):
            emote = emote[3:]
        idle = emote[:emote.rfind('.')]
    if idx < len(pre_emotes):
        emote = pre_emotes[idx]
        pre = emote[:emote.rfind('.')]
        # Without an idle we still need one. So, turn preanim into idle.
        if idle == '-':
            idle = pre
            pre = '-'
        else:
            timestring += f'{pre} = 0\n'
    name = idle[idle.rfind('/')+1:].capitalize()
    string += f'{idx+1} = {name}#{pre}#{idle}#0#\n'

File.write('\n[Time]\n')
File.write(timestring)
File.write('\n')
File.write('[Emotions]\n')
File.write('number={}\n'.format(emote_number))
File.write(string)

File.write('\n[SoundN]\n')
# a = 0
# while a < emote_number:
#     a += 1
#     File.write('{} = 0\n'.format(a))
File.write('\n[SoundT]\n')
# a = 0
# while a < emote_number:
#     a += 1
#     File.write('{} = 0\n'.format(a))

input("Done! Press ENTER to exit.")
