import os
import sys

from shutil import copy2

os.chdir(os.path.dirname(__file__))

print()

state = input('Type (background or foreground): ').lower()

if state.lower() == 'foreground':
    names = ('defensedesk', 'helperdesk', 'prosecutiondesk',
            'prohelperdesk', 'stand', 'judgedesk')
elif state.lower() == 'background':
    names = ('defenseempty', 'helperstand', 'prosecutorempty',
            'prohelperstand', 'witnessempty', 'judgestand')
else:
    input("Unable to continue - unrecognized type '{}'!".format(state))
    quit()

i = -1
frames = 0
for bg in os.listdir():
    if bg.lower().endswith('.png'):
        if frames == 0:
            i += 1
        Dir = os.path.join(os.getcwd(), 'bg{}'.format(i))
        if not os.path.exists(Dir):
            os.makedirs(Dir)
        copy2(bg, '{}/{}.png'.format(Dir, names[frames]))
        print('{}/{}.png'.format(Dir, names[frames]))
        frames = (frames + 1) % 6

input('Donezo')
