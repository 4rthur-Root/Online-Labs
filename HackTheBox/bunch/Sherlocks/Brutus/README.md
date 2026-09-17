Sherlock Scenario
In this Sherlock, you will familiarize yourself with Unix auth.log and wtmp logs. We'll explore a scenario where a Confluence server was brute-forced via its SSH service. After gaining access to the server, the attacker performed additional activities, which we can track using auth.log. Although auth.log is primarily used for brute-force analysis, we will delve into the full potential of this artifact in our investigation, including aspects of privilege escalation, persistence, and even some visibility into command execution.


cat auth.log | grep "Failed password"
cat auth.log | grep "login" 
wtmp is a binary file on Linux, Solaris, and BSD systems located at /var/log/wtmp that maintains a historical record of all user logins and logouts.  The "w" stands for "who," indicating it tracks user identity and timestamps for system access. 

Unlike utmp, which records only currently logged-in users, wtmp preserves the complete history of user activity since the last system boot.  Because it is a binary file, it cannot be read with standard text editors; instead, administrators use commands like last to view its contents.

utmpdump is a Linux utility used to dump UTMP and WTMP files in raw format for examination, debugging, and forensic analysis.  It is part of the util-linux package, which is pre-installed on most Linux distributions such as Ubuntu and Kali Linux. 

For advanced output formats like JSON, TSV, or CSV, users can install a separate Go-based version from GitHub (e.g., neko-neko/utmpdump). 

The tool converts binary system logs into human-readable text. These logs include:

/var/run/utmp: Contains information about currently logged-in users. 
/var/log/wtmp: Records all historical logins and system reboots. 
/var/log/btmp: Tracks failed login attempts.
Key capabilities include:

Dumping: Converting binary logs to ASCII text using utmpdump filename. 
Reintegrating: Writing edited text files back into binary logs using utmpdump -r < ascii_file > wtmp. 
Forensics: Detecting log file tampering or corruption by comparing raw dumps. 

utmpdump wtmp | grep root 

Q1- Analyze the auth.log. What is the IP address used by the attacker to carry out a brute force attack?

Q2- The bruteforce attempts were successful and attacker gained access to an account on the server. What is the username of the account?

Q3- Identify the UTC timestamp when the attacker logged in manually to the server and established a terminal session to carry out their objectives. The login time will be different than the authentication time, and can be found in the wtmp artifact.

Q4- SSH login sessions are tracked and assigned a session number upon login. What is the session number assigned to the attacker's session for the user account from Question 2?

Q5- The attacker added a new user as part of their persistence strategy on the server and gave this new user account higher privileges. What is the name of this account?

Q6- What is the MITRE ATT&CK sub-technique ID used for persistence by creating a new account?
T1136.001
The MITRE ATT&CK technique ID for creating a new account to maintain persistence is T1136 (Create Account).  This technique is categorized under the Persistence tactic (TA0003) and includes three specific sub-techniques:

T1136.001: Local Account
T1136.002: Domain Account
T1136.003: Cloud Account
Adversaries use these methods to establish secondary credentialed access that does not require persistent remote access tools. 

Q7- What time did the attacker's first SSH session end according to auth.log?

Q8- The attacker logged into their backdoor account and utilized their higher privileges to download a script. What is the full command executed using sudo?

