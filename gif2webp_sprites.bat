for /R %%i in (*.gif) do (gif2webp.exe -f 0 -m 6 -min_size "%%i" -o "%%~dpni.webp")