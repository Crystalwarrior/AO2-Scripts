import os
import sys

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

os.chdir(os.path.dirname(__file__))

state = ""
to_numb = 0
from_numb = int(input("From where: "))
raise_numb = int(input("With how many: "))

for button in reversed(os.listdir()):
    if button[0:6] == "button" and is_int(button[6]):
        if button[-5] == "f":
            to_numb = -8
            state = "off"
        else:
            to_numb = -7
            state = "on"
        button_numb = int(button[6:to_numb])
        new_numb = button_numb + raise_numb
        if button_numb >= from_numb:
            os.rename(button, 'button{}_{}.png'.format(new_numb, state))
            print('Renaming button{}_{}.png to button{}_{}.png'.format(button_numb, state, new_numb, state))
input('Donezo')
# while F in os.listdir():
#     os.rename(F, 'button{}_{}.png'.format(i, state))
#     i+=1

