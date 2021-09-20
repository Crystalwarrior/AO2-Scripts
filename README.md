[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I51SHXD)

All of the python scripts require Python version 3 and above.
Image Magick is also reccomended for batch-cropping, resizing, button making, etc. magic.

magick.txt:
Contains several imagemagick example commands for easier character creation. To use imagemagick effectively, click your file browser's address bar, type "cmd" and do "magick [command]" stuff.

buttonmaker.py:
A dedicated button "maker", though it's better to call this a "renamer". Drag a char.ini on top of it when it's inside a folder containing "on" or "off" buttons named after emotes, and it'll match those with the ones in char.ini and sort them out accordingly.

charmaker.py:
Creates a char.ini out of all the .png's present in the folder. Lets you input things like showname and gender, too!

sounds.py:
Read all the .wav files in the folder the script is in and output a file following the sounds.ini formatting! Can be used to ease the workload when compiling a sounds.ini with many sfx.

bgcreator.py:
Put this in the folder containing several bg image files (could be more than 6) and this bad boy will ask you if you want to sort them into foregrounds or backgrounds. Foregrounds = overlays/stands/etc. backgrounds = the rest of it.
Note: it is rather "dumb" and goes through the images in alphabetical order, but if you want to make it easier for yourself you could rename the images you're using the script on to get more hands-on with how the background folder is structured without breaking your mind by using numbers or letters, e.g. 1.png 2.png 3.png 4.png etc.

renumberer.py:
Oh yeah, I made this while making update on Mary in retribution and maybe someone gonna need this. This script help you in the situation if you made an emote and want to put it somewhere in the middle of the list, but now have to rename all the button. This automate this for you. Put it next to the buttons and start it up. It ask two parameter: From where it start the renumbering (Example: if you input 10 then button_10 gonna be the first one it rename) and with how many it add to the numbers in the button's name. After that you are done. --Fantos
