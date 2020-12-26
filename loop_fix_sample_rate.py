import os
from os import path

old_sample_rate = float(input("What was the original sample rate? "))
new_sample_rate = float(input("What is the new sample rate? "))

for file in os.listdir(os.getcwd()):
    name = file.rsplit(".",1)[0]
    if file.rsplit(".",1)[-1] == "opus" and path.exists(name + ".opus.txt"):
        print('\n')
        print(name)
        f = open(name + ".opus.txt", "r")
        lines = f.readlines()
        f.close()
        new_lines = []
        for line in lines:
            args = line.split('=')
            command = args[0].strip()
            samples = int(args[1].strip())
            new_samples = int(samples * (new_sample_rate / old_sample_rate))
            new_line = f'{command}={new_samples}'
            print(f'Converting {line.strip()} to {new_line.strip()}')
            new_lines.append(new_line)
        f = open(name + ".opus.txt", "w")
        f.write('\n'.join(new_lines))
        f.close()