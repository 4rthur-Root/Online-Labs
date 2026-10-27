# README
Welcome to Tabletop exercises

Your exercise will start soon, but first, here's a quick tour of how everything works.

Real-time simulation: Everyone sees the same injects and decides actions together. Your choices shape the narrative and outcomes in real time.

Collaborative evaluation: Each decision helps assess your team's response. After voting, wait for your facilitator, results set the rhythm of the exercise.

Smart notes: You can take notes anytime. After each decision, we'll suggest action-focused notes you can add automatically.

Navigation & tools: Use the timeline on the left to explore past injects, and access tools or references from the sidebar anytime. You can also filter to focus only on narratives if you prefer a clean view.

Narrative update: Initial Access

It's launch day. NeuralNexus ships at 17:00 UTC, and the studio is staging final build artifacts while Marketing coordinates the release. Last night's threat hunt confirmed Pinstripe Moth is still inside: THM-SREYES is still beaconing to 45.147.230.131, and the svc-studioops credentials, which the deploy pipeline depends on, are in the attacker's hands. Nothing has been remediated, and leadership has confirmed the launch goes ahead.

At 09:42 UTC, Splunk shows svc-studioops logging into BUILD-01 from THM-SREYES. The account normally only authenticates from the CI/CD orchestrator during scheduled build windows using Kerberos. This logon used NTLM, fell outside any deployment job, and lasted under four minutes. Jada Collins confirms she has scheduled no manual build activity today. A small number of process and system events from that session haven't been reviewed yet.

Rotating svc-studioops now will break the release pipeline. Isolating THM-SREYES takes a developer offline on launch day. Seven hours and eighteen minutes to launch.

```
Stage artefact

Splunk ES - Notable Event                      
Severity: High
Triggered: 2026-09-11 09:42:17 UTC
Rule: Unusual Source Host for Privileged Service Account

Account:  svc-studioops  [WATCHLIST - compromised, added 2026-09-10]
Logon:    4624, Type 3, NTLM (expected: Kerberos)
Source:   THM-SREYES (10.60.10.41)  - expected: CI-01 only
Target:   BUILD-01 (10.60.10.20)
Jenkins:  no scheduled job
Session:  09:42:17 - 09:45:58 (3m41s)

BUILD-01 follow-up activity:
  Sysmon: no data (agent not reporting)
  Security log: 3 events in session window - not triaged

Status: New - unassigned
```

![Q1](./shots/Q-1.png)

# My-choice

P1: A known-compromised pipeline account is on the build server on launch day, so declare a High incident and bring in Dana Brooks and Jada Collins to review the BUILD-01 session and pipeline integrity.

## Team decision analysis

This was the most effective call available in this phase, and it reflects sound incident-command judgment. Given that svc-studioops is a known-compromised account and it just appeared on BUILD-01, the day of launch, this is no longer a routine anomaly — it merits a High severity classification with the right stakeholders engaged immediately. Looping in Dana Brooks for command decisions and Jada Collins for pipeline-specific context ensures you get accurate technical insight into build integrity without the overreaction of a full leadership-level Critical declaration before tampering is confirmed, which is why the all-hands option ranked lower despite good instincts. The downgraded options, logging it as Low severity, keeping it confined to SOC L2 review, or worse, marking it Informational, all underestimate the risk of a compromised credential touching your deployment pipeline on launch day, and would have cost you valuable time if sabotage is already underway. Your choice balances urgency with proportionality, keeping the right people in the room without prematurely triggering business-level alarm.

![an](./shots/analysis-1.png)

![q2](./shots/Q-2.png)

my choice was B

Pull and triage the three unreviewed Security log events from the 09:42-09:45 UTC session window on BUILD-01 to determine exactly what the attacker executed or accessed.

## Team decision analysis

This was the strongest move available because with Sysmon data gone silent, the native Security event logs are the only direct window into what the attacker actually did during that session, and triaging them first gives you concrete ground truth before expanding scope elsewhere. Reviewing file and artifact timestamps was a reasonable follow-up but works better once you know what commands were run, and mapping svc-studioops activity across the environment is valuable for scoping but doesn't tell you what happened on BUILD-01 itself in those critical three minutes. Investigating the Sysmon outage is important forensic work, but it's secondary to understanding the attacker's actions, and pausing analysis entirely until telemetry is restored is the weakest choice since it sacrifices momentum on launch day while the clock is running against you. Your instinct to go straight to the available evidence of what was executed reflects a sharp evidence-first mindset under time pressure.

![an](./shots/analysis-2.png)

!Q3 here 
chose D 
Work with Jada Collins to rotate the svc-studioops password in Jenkins and restrict the account to CI-01, cutting off the stolen credentials without stopping the pipeline.

Team decision analysis

This was the most precise and business-aligned containment move on the table, directly neutralizing the compromised credential that enabled the sabotage while preserving the launch-critical pipeline by scoping the account to CI-01. Isolating THM-SREYES and blocking the C2 IP both address real exposure points but leave the stolen svc-studioops credential usable elsewhere, so they're reasonable but incomplete compared to actually rotating it. Killing the beacon process and Run key tackles only the original beachhead, not the pipeline account the attacker pivoted to, and disabling svc-studioops entirely would have severed the threat but at the cost of halting the build on launch day, an outcome you avoided by working with Jada Collins on a scoped rotation instead. This decision shows strong judgment in balancing security containment against business continuity at the most sensitive possible moment.

Q4 
chose 
Audit every scheduled task and deploy script on BUILD-01 and CI-01 that runs as svc-studioops, removing anything Jada doesn’t recognise before updating the rest with the new password.

Team decision analysis

Confirming the pipeline functions post-rotation is a sensible operational check, but it's moderately effective at best because it validates that credentials work without actually confirming the attacker didn't leave something behind during their window of access. The stronger moves were auditing every scheduled task and deploy script running as svc-studioops to hunt for unauthorized persistence, and verifying the staged build's hash against the QA-signed version, since both directly address whether sabotage already occurred, which is the real risk on launch day rather than whether the account merely still functions. Updating the password everywhere restores operations but, like your chosen action, doesn't hunt for tampering, which is why both rank behind the integrity-focused options. Logging the rotation without any testing, and worse, skipping the hash verification, would leave you dangerously exposed to shipping a sabotaged build, so your instinct to test was reasonable, just not pointed at the highest-priority risk of this phase.

Q5 
chose 
B 
Brief Dana Brooks and launch leadership that the attacker has reached the build host, so they understand the risk to release integrity before the 17:00 UTC launch.

This was the right call for this moment: with the attacker confirmed on the build host just hours before a public launch, leadership needs an accurate risk picture now so they can weigh a possible delay or contingency plan with full information, rather than being surprised at 17:00. Keeping Alex Morgan and Riley Tran on continuous monitoring is valuable but tactical, not a substitute for ensuring decision-makers understand the stakes, while engaging DFIR, legal, and the insurer is prudent longer-term given the repeat targeting but doesn't address the immediate launch-day decision. Looping in the national cyber crime unit at this stage is premature given the limited external impact so far, and asking Jada to review logs alone misses that this is fundamentally a leadership communication gap, not a technical one, which is why it ranked lowest. Your choice correctly recognized that informed executive judgment is the critical path item right now, ahead of further technical tasking.


# Narrative update: Lateral Movement & Privilege Escalation

The session on BUILD-01 wasn't idle. At 10:07 UTC, svc-studioops opened a WinRM session from BUILD-01 to BAK-01, the backup server nobody has checked yet. That's 20 minutes after the original logon ended, before any containment took effect. Something on BUILD-01 is still acting as svc-studioops, and Sysmon there is still blind. Within a minute, a new local account, backup-svc, was created on BAK-01 and added to Backup Operators. PowerShell logging then shows the attacker enumerating scheduled tasks and the permissions on C:\Backups before disconnecting. Nobody requested either change.

At 10:24 UTC, Michelle Smith calls the SOC. The official NeuralNexus account has just posted that the launch is "delayed due to technical issues", with a link to an "early access build" hosted off-site. It has 400 reposts and counting, and Michelle can't log in to take it down.

Six hours and thirty-six minutes to launch. Pinstripe Moth is no longer being quiet.


Stage artefact

Splunk ES - Notable Event                      
Severity: High
Triggered: 2026-09-11 10:07:52 UTC
Rule: Privileged Account - Group Modification

Account:  svc-studioops  [WATCHLIST - compromised]
Logon:    WinRM, BUILD-01 -> BAK-01 (10:07:52 - 10:11:36)
Source process on BUILD-01: unknown - Sysmon not reporting

BAK-01:
10:08:41  4720  Local account created: backup-svc
10:08:47  4732  backup-svc added to Backup Operators
10:09:12  PS    Get-ScheduledTask
10:09:30  PS    Get-Acl C:\Backups

Related: SIEM-09421 (BUILD-01, 09:42)

Q6 chose 
P1: Declare a High incident across the pipeline and backups with Dana, Jada and Luke, holding off on leadership and Legal until sabotage intent is confirmed.

Escalating to a High incident and pulling in Dana, Jada and Luke was a solid, effective response to the backups and pipeline exposure, but holding leadership and Legal back once the attacker has reached backups and hijacked the official launch account understates the business-facing nature of what just happened. The top option recognized that a hijacked social channel is already a public-facing event with reputational and possibly legal dimensions that can't wait for confirmed sabotage intent, which is why full Critical escalation with Comms and Legal included was the strongest move. Treating BAK-01 and the account hijack as separate, lower-severity issues, or folding them quietly into the existing case, underestimates how these two threads now intersect with the live launch, and marking alerts Informational at this stage would have been a serious miss given the account takeover is already externally visible. Your call captured the internal technical response well but was a step behind on recognizing that external stakeholders needed to be engaged immediately, not after further confirmation.

analysis6.png

Q7 chose 
Most effective
Pull BUILD-01’s own Windows event logs (4688, 4698, 5156) to find what’s still running as svc-studioops, since Sysmon there is blind.

This was the most effective choice because it directly compensates for the Sysmon blind spot on BUILD-01 by going straight to native Windows event logs, 4688 for process creation, 4698 for scheduled task creation, and 5156 for network connections, giving you the clearest possible picture of what svc-studioops is actively doing on the host most critical to launch integrity right now. Checking pipeline logs for unauthorized jobs or config edits is a strong complementary step but is secondary to establishing what's actually executing on the compromised host itself, and mapping the full lateral movement timeline, while useful for scoping, is less urgent than real-time visibility into ongoing activity. Analysing BAK-01's permission queries matters for backup integrity but is a narrower concern than the build host at this moment, and reviewing the social account's login history, while necessary eventually, does nothing to address the active technical threat to the launch pipeline, which is why it ranked lowest here. Your decision correctly prioritized closing the most dangerous visibility gap at the most sensitive point in the infrastructure.

Q8

Isolate BUILD-01, since it’s running an unknown process as svc-studioops and Sysmon can’t see it.

Team decision analysis

Isolating BUILD-01 is a reasonable containment reflex given the unknown process and the blind Sysmon gap, but it's a moderately effective choice because it only addresses one half of the active crisis, leaving the hijacked social account live and the backups exposed. The strongest move was recovering the NeuralNexus account and revoking sessions, since that's the most visible, time-critical harm with a public audience right before launch, while isolating BAK-01 and disabling backup-svc protects your last line of defense without disrupting the pipeline itself, both outranking a BUILD-01-only isolation. Disabling svc-studioops entirely across both hosts is more disruptive than necessary at this stage, and killing WinRM environment-wide is a blunt, high-collateral move that would hamper your own response capability, which is why it ranked lowest. Your instinct to contain the host with the biggest blind spot was sound, but it came at the expense of the more urgent public-facing and backup-protection priorities this phase called for.

Q9 chose 
Validate BAK-01’s backup data against known-good checksums before relying on it for any restore or rebuild.

Team decision analysis

This was the most effective decision in this phase, because before any restoration, credential rotation, or re-hardening work matters, you need certainty that the backup data itself hasn't been tampered with, especially with an attacker who reached BAK-01 and had visibility into backup permissions. Restoring telemetry on BUILD-01 and BAK-01 and rotating credentials are both important follow-on steps, but they don't answer the core question of whether the backups are trustworthy, which is why they rank below your choice. Rebuilding BAK-01 from a verified image is premature without first confirming what "verified" actually means in this context, and resetting Backup Operators membership while resuming jobs without validation would risk propagating a compromised or sabotaged baseline straight into production, making it the weakest option here. Your prioritization of data integrity before operational trust reflects exactly the discipline needed when backups themselves are a suspected target.

Q10 chose 
Update leadership, Legal and PR on the public impersonation and the attacker’s move onto the backups, so they can manage launch messaging and the go/no-go decision.
Team decision analysis

Updating leadership, Legal and PR was an effective, necessary action given the go/no-go decision bearing down, but it was a step behind the top priority: the fraudulent post is live and actively misleading the public right now, so escalating directly to the social platform's security team for emergency recovery and takedown addresses the most time-sensitive, externally visible harm first. Alerting Luke and Jada about the untrustworthy backups was a reasonable parallel technical notification but ranks below both the platform escalation and the leadership briefing since it doesn't address the public-facing crisis or the decision-makers who need to act on it. Reporting to the cyber crime unit is appropriate but not as urgent as stopping the active impersonation, and declaring a company-wide crisis with external PR involvement at this stage is premature and would consume response bandwidth you need focused on containment. Your choice correctly engaged the people who own the go/no-go call, but the fraudulent post itself needed to be shut down with equal or greater urgency.


Narrative update: Goal Execution

The backup-svc account wasn't recon. It was setup. At 10:11 UTC, in the last seconds of its session on BAK-01, svc-studioops created a scheduled task called BackupMaintenance, set to run as SYSTEM from 10:52. Since then it has run purge-artifacts.ps1 every 15 minutes. Last night's gold master is gone, along with the nightly archive on FS-ARCHIVE and every shadow copy. Jada Collins confirms one verified restore point remains. The next run is at 11:37.

BUILD-01's Security log finally gives up its secret. One of the three events from the 09:42 session was a scheduled task creation: DeployPrep, set to run once as svc-studioops at 16:55 and replace the signed release package with a modified build.

Pinstripe Moth's plan is now clear: destroy every clean restore point, then ship their own build under the studio's name. Michelle is still locked out of the official account, and the fake "early access" build is still circulating.

11:25 UTC. Twelve minutes until the last backup is gone. Five hours and thirty-five minutes until launch.


Stage artefact

Splunk ES - Notable Event                      
Severity: Critical
Triggered: 2026-09-11 10:52:03 UTC
Rule: Suspicious Scheduled Task Execution

BAK-01 - Task "\Microsoft\Windows\BackupMaintenance"
Created:  10:11:20 by svc-studioops (4698)
Run as:   SYSTEM, every 15 min
Action:   powershell -ExecutionPolicy Bypass -File C:\Windows\Temp\purge-artifacts.ps1

10:52  Deleted  GoldMaster_2026-09-10.vhdx
10:52  vssadmin delete shadows /all /quiet
11:07  Deleted  \\FS-ARCHIVE\Nightly\NeuralNexus\2026-09-10\*
11:22  Deleted  build_0911_0600.zip

Restore points remaining: 1     Next run: 11:37

BUILD-01 - Security log (09:43:10, previously untriaged)
4698  Task "DeployPrep" created by svc-studioops
      Runs once 16:55 as svc-studioops - replaces release package


Q11 chose

P0: Backups are being destroyed and a malicious build is staged to ship, so declare a Critical incident and bring leadership, Legal, Jada, Luke and Comms into the launch decision immediately.

This was the correct call, and arguably the clearest escalation decision in the exercise so far: with backups actively being destroyed and a malicious build staged for shipment, the direct line to the launch itself, this is no longer a technical containment question but an existential threat to release integrity that demands every relevant decision-maker in the room immediately. Holding off on leadership and Legal, as the High-severity option did, would have delayed the one decision that matters most right now, whether to ship at all, and the moderate or Low-severity framings dangerously understate that the sabotage has reached the point of threatening the actual deliverable. Marking it Informational at this stage, given everything already confirmed about backup destruction and a tampered build, would represent a critical failure to recognize an unfolding worst-case scenario. Your decision to pull in leadership, Legal, Jada, Luke and Comms together reflects exactly the urgency and cross-functional coordination this moment demanded.



Q12 chose 
Review the rest of BUILD-01’s 09:42 session logs for anything else planted on that host. hesitated with Sweep Splunk for every svc-studioops logon, WinRM session and scheduled task creation across all hosts to find any persistence beyond BAK-01 and BUILD-01.

Team decision analysis

Revisiting BUILD-01's earlier session logs is a reasonable follow-up, but it's moderately effective because it looks backward at the original intrusion window rather than addressing the two most pressing unknowns right now: the full scope of svc-studioops persistence across the environment, and what exactly the malicious DeployPrep payload was set to ship at 16:55. Sweeping Splunk for every svc-studioops logon and scheduled task across all hosts was the strongest option because it answers the critical question of whether this sabotage extends beyond BAK-01 and BUILD-01 before you can call the environment contained, and analysing the staged payload directly tells you exactly what nearly shipped, both more urgent than re-reading an already-reviewed session window. Checking C2 traffic to 45.147.230.131 is useful corroboration but secondary to scope and payload analysis, and auditing AD/GPO for svc-studioops artifacts, while thorough, is the least time-critical path given no indication yet that persistence moved through Group Policy. Your choice kept useful forensic rigor but didn't prioritize the two threads with the most direct bearing on the ship/no-ship decision and full remediation scope.


Q13 chose 
Disable the DeployPrep task on BUILD-01 so it can’t replace the signed release package at 16:55. (prioritysing launch)

Team decision analysis

Disabling DeployPrep was an effective action to protect the signed release package, but it ranked just behind the top priority because the BackupMaintenance task and purge-artifacts.ps1 on BAK-01 are on an even tighter clock, set to run at 11:37, and destroying your last restore point would remove any fallback if the build itself turns out to be compromised. Stopping that purge first preserves your recovery option, which is why it edged out halting DeployPrep as the single most urgent move. Blocking the C2 IP and restricting WinRM on the pipeline hosts both reduce the attacker's ongoing capability but don't address either scheduled task directly ticking toward execution, and disabling svc-studioops entirely, while thorough, risks disrupting legitimate pipeline operations without surgically stopping the two specific malicious tasks already in motion. Your choice correctly targeted one of the two live threats, just not the one with the narrower fuse.


14 chose 
Verify the staged release package against the QA-signed hash, and rebuild it from a known-good source on a clean runner if it doesn’t match.

Team decision analysis

Verifying the staged release package against the QA-signed hash was an effective and necessary step before shipping, but it ranked just behind securing your last clean restore point, since without a verified, segregated recovery point safely off BAK-01, you'd have no fallback if the rebuild itself turns out compromised or if further sabotage is discovered. Preserving that restore point first is the foundation everything else depends on, which is why it edged out package verification for top priority. Reissuing svc-studioops credentials into the pipeline is a reasonable operational step but doesn't address data or build integrity, and triggering a fresh gold master backup from BUILD-01 is risky since that host's own trustworthiness hasn't been fully re-established yet. Resuming nightly backup jobs on BAK-01 without first confirming the server is clean and the purge threat fully neutralized would be premature and is why that option ranked lowest. Your instinct to validate the build before shipping was sound, just one step behind locking down your recovery safety net first.



Q15 chose 
Brief the launch steering committee on the staged release swap, backup loss and current containment status so they can make the 17:00 go/no-go call.

Team decision analysis

This was the most effective action for this moment, because with the launch window closing in, the steering committee needs a complete, concrete picture of the staged release swap, the backup loss and where containment currently stands in order to make the one decision that actually matters: whether NeuralNexus ships at 17:00. Formalizing Dana Brooks as Incident Commander and declaring Severity 1 to executive leadership are both sensible structural moves, but they organize the response rather than directly equipping the people who must decide on the launch itself, which is why they trail behind a direct briefing. Reporting to the cyber crime unit is appropriate but not time-critical compared to the go/no-go decision bearing down within the hour, and broadcasting an emergency alert to all staff and external stakeholders before any validation or leadership briefing would be reckless, risking panic and reputational harm based on incomplete information. Your decision correctly recognized that the steering committee's informed judgment, built on everything you now know about the sabotage, was the single most consequential output this phase could produce.





















# FINAL

Nice work completing the exercise!
Sabotage
Date:
1 participants
Narrative conclusion
points: 127
/150
In the final hours before launch, your swift identification of the staged release swap and the backup purge attempt let you preserve a clean restore point and a verified build, and your decision to brief the steering committee directly gave leadership the facts they needed to make an informed 17:00 go/no-go call; the launch proceeded on schedule with a short public statement attributing the earlier delay to "routine pre-launch verification," while the full incident was handed off to your crisis management team to manage stakeholder communications, law enforcement liaison and the longer recovery from Pinstripe Moth's second intrusion. Well done holding the line between technical containment and business-critical decision-making under real time pressure, that balance is exactly what separates organizations that ship safely from those that don't. Keep this momentum by running tabletop exercises like this one regularly, so the instincts you sharpened today, fast escalation, evidence-first triage, and clear executive briefings, stay ready for whenever Pinstripe Moth or another adversary comes back.






ALL ANALYSIS ARE LIVE AND MADE BY AI I THINK