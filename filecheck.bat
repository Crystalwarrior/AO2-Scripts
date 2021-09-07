@echo off
echo Checking the folder contents against manifest.txt...
echo The files you're missing are:> missing.txt
for /f "delims=" %%x in (manifest.txt) do (
    if not exist "%~dp0%%x" (
        echo %%x is missing!
        echo %%x>>missing.txt
    )
)
echo Generating missing.txt. Check inside it to see what you need!
echo There's also extra.txt to see extra files that aren't base content.
pause