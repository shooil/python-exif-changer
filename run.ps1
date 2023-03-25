conda activate exif
$rootdir = Split-Path Parent $MyInvocation.MyCommand.Path
Set-Location -Path $rootdir
python ./main.py