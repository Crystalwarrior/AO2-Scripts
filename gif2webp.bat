for /R %%i in (*.gif) do (ffmpeg.exe -i "%%i" -y -vcodec webp -loop 0 -pix_fmt yuva420p "%%~pni.webp")