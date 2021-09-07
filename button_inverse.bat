if not exist "_temp" mkdir _temp
move *_off.png _temp
ren *_on.png *_off.png
cd _temp\
ren *_off.png *_on.png
cd ..
move _temp\* .
rd _temp\