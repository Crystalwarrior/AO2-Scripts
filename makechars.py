import os

File = open("characters.yaml", "w")

for char in os.listdir():
    File.write('- {}\n'.format(char))