import os
import sys

os.chdir(os.path.dirname(__file__))

File = open("soundlist.ini", "w")

input("Writing all .wav in folder to create a thing. Press ENTER to begin.")
i = 0
string = ''
for sfx in os.listdir():
	try:
		if sfx.lower().endswith(('.wav')):
			name = sfx[:sfx.find('.wav')]
			i += 1
			string += '{}\n'.format(name)
			print('{} = {}'.format(i, name))
	except:
		continue

File.write(string)

input("Done! Press ENTER to exit.")
