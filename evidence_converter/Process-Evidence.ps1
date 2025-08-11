<#
.SYNOPSIS
    Converts evidence descriptions to /evidence_add commands.
.DESCRIPTION
    Reads an input text file with evidence entries and outputs properly formatted /evidence_add commands
.PARAMETER InputFile
    Path to the input text file containing evidence entries
.PARAMETER OutputFile
    (Optional) Path to save the output. If omitted, prints to console
.PARAMETER Pos
    (Optional) Whether to set a specific pos for all evidence, appends <owner=Pos> if included.
.EXAMPLE
    .\Process-Evidence.ps1 -InputFile "input.txt" -OutputFile "output.txt" -Pos "all"
.EXAMPLE
    .\Process-Evidence.ps1 "input.txt"  # Prints to console
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,
    
    [string]$OutputFile,

    [string]$Pos
)

# Use UTF-8 encoding for both reading and writing
$encoding = [System.Text.Encoding]::UTF8

if (-not (Test-Path $InputFile)) {
    Write-Error "Input file not found: $InputFile"
    exit 1
}

$evidenceEntries = [System.Collections.Generic.List[string]]::new()
$currentEntry = @{Image=$null; Name=$null; Desc=[System.Collections.Generic.List[string]]::new()}

function Process-CurrentEntry {
    if ($currentEntry.Image -and $currentEntry.Name) {
        $desc = $currentEntry.Desc -join "`n"
        $escapedDesc = $desc.Replace('"', '\"')
        if ($OutputFile) {
            $entry = "/evidence_add `"$($currentEntry.Name)`" `"<owner=$Pos>`n$escapedDesc`" $($currentEntry.Image)%"
        }
        else {
            $entry = "/evidence_add `"$($currentEntry.Name)`" `"$escapedDesc`" $($currentEntry.Image)%"
        }
        $evidenceEntries.Add($entry)
    }
}

# Read input with proper encoding
$lines = [System.IO.File]::ReadAllLines($InputFile, $encoding)

foreach ($line in $lines) {
    if ($line -match '\.png$') {
        Process-CurrentEntry
        $currentEntry.Image = $line.Trim()
        $currentEntry.Name = $null
        $currentEntry.Desc.Clear()
        continue
    }

    if (-not $currentEntry.Name) {
        $currentEntry.Name = $line.Trim()
        continue
    }

    $currentEntry.Desc.Add($line)
}

Process-CurrentEntry

# Output with proper encoding
if ($OutputFile) {
    [System.IO.File]::WriteAllLines($OutputFile, $evidenceEntries, $encoding)
    Write-Host "Output saved to $OutputFile with UTF-8 encoding"
} else {
    $evidenceEntries | ForEach-Object { $_ }
}