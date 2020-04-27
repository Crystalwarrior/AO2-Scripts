# Powershell script
# on Windows Explorer, shift + right-click a directory and copy its path
# paste the path in $dir
$dir = "."

# get all files in the directory
$ToNatural = { [regex]::Replace($_, '\d+', { $args[0].Value.PadLeft(20) }) }
$images = Get-ChildItem $dir -Name -Include *.png | Sort-Object $ToNatural
$images
$outputName = $dir + "\output.webp"

img2webp -min_size -mixed $images -d 3 -q 85 -o $outputName