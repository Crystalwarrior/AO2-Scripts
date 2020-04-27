import os

File = open("backgrounds.yaml", "w")

files = filter(os.path.isdir, os.listdir(os.getcwd()))

for char in files:
    File.write('- {}\n'.format(char))
