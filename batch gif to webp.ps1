# Powershell script
# on Windows Explorer, shift + right-click a directory and copy its path
# paste the path in $dir
$dir = "."

# get all files in the directory
$images = Get-ChildItem $dir -Filter *.gif

# loop through every images
foreach ($img in $images) {
  # output file will be written in the same directory 
  # but with .webp extension instead of old extension
  $outputName = $img.DirectoryName + "\" + $img.BaseName + ".webp"

  # copy-paste the path to cwebp program 
  # and set its input and output parameters
  # more options https://developers.google.com/speed/webp/docs/cwebp
  gif2webp -min_size -mixed -q 85 $img.FullName -o $outputName
}