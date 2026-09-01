# SCENARIO REVEAL

What the scenario is all about ?

it is one of the most classic ways of an attack involving C2.

Firefox download stager : The place where the payload was downloaded from http://w1ndowsupdate.com:8080/update.exe.hta

Execution update.exe.hta: this execution let's to the creation of agent1

Creation of C2 agent1 Powershell process: created by update.exe.hta it is a powershell process that was communicating with the malicious IP 3.140.33.120 on port 9001

Persistence via registry Run keys: active persistence maintained via Registry run keys to keep contact with the system 

Privilege escalation via env variable: Invoke ..... script was used to gain an elevate session that led to second agent

Creation of C2 agent2 Powershell process: it was created and this one had admin rights 

Reconnaissance tools execution: reconnaissance tools were run such as whoami

Failed process injection attempts: attempts to make process injection in the registry files .

Various shell commands: navigating in the filesystem, to discovery files, dns queries ,use powershell, create something in temp.

Creation of C:\Temp: It was not there before , was created by powershelll execution 

Staging of Alice\Documents into C:\Temp\1.zip : staging the files to the temp folder upload and delete it 

Upload of 1.zip via agent2: upload of the staging via agent 2

All these were primarly shown in wireshark and splunk .

it was not muuch thouh 4 mb 
1 system, persitence, exfiltration . It shows what an attacker can do to actually steal important stuff .
