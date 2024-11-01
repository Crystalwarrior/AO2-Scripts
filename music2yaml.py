import os
import subprocess
import sys

from shutil import copy2


def check_deps():
    py_version = sys.version_info
    if py_version.major < 3:
        print(
            "tsuserver3 requires at least Python 3! Your version: {}.{}".format(
                py_version.major, py_version.minor
            )
        )
        sys.exit(1)

    try:
        import tinytag
    except ModuleNotFoundError:
        print("Installing dependencies for you...")
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--user",
                    "tinytag",
                ]
            )
            print(
                "If an import error occurs after the installation, try "
                "restarting the server."
            )
        except subprocess.CalledProcessError:
            print(
                "Couldn't install it for you, because you don't have pip, "
                "or another error occurred."
            )



arg = ""
if len(sys.argv) > 1:
    arg = sys.argv[1]

scandir = os.getcwd()
yaml_name = 'music.yaml'
droppedFile = None
if arg != "":
    if os.path.isfile(arg):
        droppedFile = open(arg, "r")
    elif os.path.isdir(arg):
        scandir = arg
        yaml_name = f'{scandir}.yaml'

os.chdir(os.path.dirname(scandir))
use_lengths = input(
    'Analyze song lengths and put them in length:? (tinytag module required) (y/n)').lower() == 'y'
if use_lengths:
    check_deps()
    from tinytag import TinyTag
    print('Using tinytag module for song lengths...')

File = open(yaml_name, "w")
File.write('- use_unique_folder: False #If true, this music will be contained entirely within its own folder e.g. base/music/<yaml name>/*.mp3\n')


def set_category(category_name):
    File.write(f'- category: =={category_name}==\n')
    File.write('  songs:\n')
    print(f'Current category: {category_name}')
    return category_name


def add_song(song_name):
    duration = -1
    fname = song_name
    if use_lengths:
        tag = TinyTag.get(fname)
        duration = tag.duration
    File.write(
        '    - name: "{}"\n'.format(fname))
    File.write('      length: {}\n'.format(duration))
    print("Name: {} Length: {}".format(song_name, duration))


if droppedFile:
    input("Writing .mp3, .ogg, .opus, .wav and .m4a and categorizing them based on file argument to music.yaml. Press ENTER to begin.")
    current_category = ""
    Err = None
    for line in droppedFile.readlines():
        try:
            line = line.rstrip()
            if line.lower().startswith('[mod]'):
                continue
            if line.lower().endswith(('.mp3', '.ogg', '.opus', '.wav', '.m4a')):
                try:
                    if line.lower().endswith(':') and current_category != line[:-1]:
                        current_category = set_category(line[:-1])
                    add_song(line)
                except:
                    if not Err:
                        Err = open("music_errors.txt", "w")
                    Err.write('Error for {}\n'.format(line))
                    input(
                        "Unable to process song: {}! Press ENTER to continue.".format(line))
        except:
            continue
else:
    input(f"Writing all .mp3, .ogg, .opus, .wav and .m4a present in current folder/subfolders to {yaml_name}. Any subfolders will be made as new categories. Press ENTER to begin.")

    def recursive_songlist(dir, current_category = ""):
        for f in os.scandir(dir):
            if f.is_file():
                if f.name.lower().startswith('[mod]'):
                    continue
                if f.name.lower().endswith(('.mp3', '.ogg', '.opus', '.wav', '.m4a')):
                    song_path = os.path.relpath(f.path, os.getcwd()).replace("\\", "/")
                    cat = os.path.relpath(os.path.dirname(f.path), os.getcwd()).replace("\\", " - ")
                    if current_category != cat and cat != ".":
                        current_category = set_category(cat)
                    add_song(song_path)
            elif f.is_dir():
                print('Folder: ' + f.path)
                recursive_songlist(f.path, current_category)

    recursive_songlist(scandir)

input("Done! Press ENTER to exit.")
