import os
import shutil
import sys
import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

directory = os.path.dirname(__file__)
os.chdir(directory)

File = open("char.ini", "w")

File.write('[Options]\n')
File.write('name = {}\n'.format(os.path.basename(directory)))
File.write('showname = {}\n'.format(input("Please input showname.")))
File.write('side = {}\n'.format('wit'))
File.write('gender = {}\n'.format(input("Please input gender.")))

input("Writing all images in folder to char.ini. Press ENTER to begin.")
i = 0
string = ''
timestring = ''
for emote in natural_sort(os.listdir()):
	try:
		if emote.lower() != "char_icon.png" and emote.lower().endswith(('.png', '.gif', '.webp', '.apng')):
			name1 = emote
			prefix = ''
			if emote.lower().startswith('(a)'):
				name1 = emote[3:]
				prefix = '(a)'
			elif emote.lower().startswith('(b)'):
				name1 = emote[3:]
				prefix = '(b)'
			else:
				prefix = 'anim'
			name = name1[:name1.rfind('.')]

			newdir = ''
			if (prefix != ''):
				Dir = '{}/{}/'.format(directory, prefix)
				if not os.path.exists(Dir):
					os.makedirs(Dir)
				print(name1)
				shutil.move('{}/{}'.format(directory, emote), '{}/{}'.format(Dir, name1))

			if prefix == '(a)':
				i += 1
				string += '{} = {}#{}#{}#0#\n'.format(i, name, '-', name)
				print('{} = {}'.format(i, name))
			elif prefix != '(b)':
				print('preanim = {}'.format(name))
				timestring += '{} = 0\n'.format(name)
	except:
		continue

File.write('\n[Time]\n')
File.write(timestring)
File.write('\n')
File.write('[Emotions]\n')
File.write('number={}\n'.format(i))
File.write(string)

File.write('\n[SoundN]\n')
a = 0
while a < i:
	a+=1
	File.write('{} = 0\n'.format(a))
File.write('\n[SoundT]\n')
a = 0
while a < i:
	a += 1
	File.write('{} = 0\n'.format(a))

input("Done! Press ENTER to exit.")
