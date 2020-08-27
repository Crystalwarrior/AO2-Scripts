import os
import sys

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

os.chdir(os.path.dirname(__file__))

arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]

if arg == "":
    raise input('No file provided! Please drag char.ini onto this script so it can rename buttons properly.')

droppedFile = open(arg, "r")

state = input('Input state (on or off): ').lower()

for line in droppedFile.readlines():
    try:
        lines = line.rstrip().split(' ')
        if lines[0] in ('[SoundN]', '[SoundT]'):
            break
        if not is_int(lines[0]):
            continue

        emote = line.split('#')[2]
        print(emote)
        for button in os.listdir():
            if button == emote + '.png':
                os.rename(button, 'button{}_{}.png'.format(lines[0], state))
                print('Made a new button for {}'.format(emote))
                break
        print('Currently on {}'.format(line))
    except:
        print("Excepted on line {}".format(line))
        continue
input('Donezo')
# while F in os.listdir():
#     os.rename(F, 'button{}_{}.png'.format(i, state))
#     i+=1

