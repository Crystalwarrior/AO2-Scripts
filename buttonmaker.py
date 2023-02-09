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
    raise input(
        'No file provided! Please drag char.ini onto this script so it can rename buttons properly.')

droppedFile = open(arg, "r")

reverse = input(
    'Rename numbered buttons back to their emotes? (y/n): ').lower() == 'y'
state = input('Input state (on or off): ').lower()

for line in droppedFile.readlines():
    try:
        words = line.rstrip().split(' ')
        if words[0] in ('[SoundN]', '[SoundT]'):
            break
        num = words[0].split('=')[0]
        if not is_int(num):
            continue

        emote = line.split('#')[2]
        print(emote)
        for button in os.listdir():
            if reverse:
                if button.lower() == f'button{num}_{state}.png':
                    os.rename(button, f'{emote.lower()}.png')
                    print(f'Renamed button {num} back to {emote}')
                    break
            elif button.lower() == emote.lower() + '.png':
                os.rename(button, 'button{}_{}.png'.format(num, state))
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
