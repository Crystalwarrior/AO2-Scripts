"What is cleanup.bat?"
It's a batch file to clean up your folder to improve filesize. Run cleanup.bat to clean up your folder of outdated base content files (Any customs that don't replace base content will not be affected)

"What is filecheck.bat?"
It's a batch file to compare all of your current folder contents against the files you are *supposed* to have. Run it to make sure you have everything you need. Note this .bat requires a manifest.txt in your folder as well!

"What is manifest.txt?"
It contains all the relative file paths for the files your folder is supposed to have, used by filecheck.bat to see if you're missing anything.

"What if I don't have manifest.txt?"
Most likely, this means you obtained the .bat files on their own from somewhere - up-to-date manifest.txt should always be included with every subsequent Content Update.

"What is missing.txt?"
You will only see this file if filecheck.bat was run, and it found missing files. This file should help you troubleshoot what files you need to obtain.

"Where do I put these?"
Make sure all .bat files and manifest.txt are located in the same folder where your Attorney_Online.exe is.