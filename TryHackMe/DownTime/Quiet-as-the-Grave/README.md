Scenario overview
TryHatMe Studios is a small, fast-rising game house with a reputation bigger than its headcount, riding the buzz around its most anticipated release yet, NeuralNexus, a platformer about a newly departed soul working through the afterlife's paperwork, one numbered ticket at a time. For a studio this size, the unreleased build and the commercial plans around it are effectively the whole business.

That is exactly what makes it a target. Financially motivated crews that once chased banks and payment processors have started turning toward creative studios, where a single leaked project can be resold or held to ransom. So when game developer Sophia Reyes opened what looked like a routine project-review file one afternoon, nobody thought twice about it.

In the days that followed, the security team began to wonder whether that quiet afternoon had been the opening move of something larger, something reaching from Sophia's workstation toward the studio's most closely held work. It would not be the first time something unwelcome had tried to move into the studio. The question for this hunt is how far it went, and whether anything got out.

Scenario objectives
Establish how the actor first gained access to the environment and how that foothold was kept alive over time.
Trace the credentials the actor used to operate, and how it moved from one system to the next.
Determine how far the actor's reach extended, including any attempts against higher-value systems such as domain infrastructure, and the broader reconnaissance it carried out along the way.
Determine what data the actor was after, how it was collected, and whether any of it ultimately left the environment.


Quiet as the Grave
Briefing
TryHatMe Studios is a small, fast-rising game house with a reputation bigger than its headcount, riding the buzz around its most anticipated release yet, NeuralNexus, a platformer about a newly departed soul working through the afterlife's paperwork, one numbered ticket at a time. For a studio this size, the unreleased build and the commercial plans around it are effectively the whole business.

That is exactly what makes it a target. Financially motivated crews that once chased banks and payment processors have started turning toward creative studios, where a single leaked project can be resold or held to ransom. So when game developer Sophia Reyes opened what looked like a routine project-review file one afternoon, nobody thought twice about it.

In the days that followed, the security team began to wonder whether that quiet afternoon had been the opening move of something larger, something reaching from Sophia's workstation toward the studio's most closely held work. It would not be the first time something unwelcome had tried to move into the studio. The question for this hunt is how far it went, and whether anything got out.

Hypothesis
Consistent with Pinstripe Moth's reported tradecraft, TryHatMe Studios may have been compromised through a lure delivered to one of its developers, giving the actor a foothold from which it used valid credentials and legitimate Windows tooling to move through the environment toward the studio's unreleased NeuralNexus work. This hunt sets out to confirm whether that activity is present, how far through the network the actor reached, and whether any of that data was taken.

Objectives
Establish how the actor first gained access to the environment and how that foothold was kept alive over time.
Trace the credentials the actor used to operate, and how it moved from one system to the next.
Determine how far the actor's reach extended, including any attempts against higher-value systems such as domain infrastructure, and the broader reconnaissance it carried out along the way.
Determine what data the actor was after, how it was collected, and whether any of it ultimately left the environment.


### Executive sumary
Subject: Financially-Motivated Intrusion Set "Pinstripe Moth" Expands From Financial Targets Into Game and Creative Studios

From: Creative Sector Threat Intake Bureau (CSTIB)

To: Assigned caseworkers: Game Development, Interactive Entertainment, and Software Studios

The CSTIB is tracking a financially-motivated activity cluster referred to by analysts as Pinstripe Moth. This is an analyst-named grouping used to correlate related activity; it is not a confirmed or attributed group. Pinstripe Moth has historically operated against banking, payment, and financial-services organisations. Reporting over recent months indicates a deliberate shift in targeting toward small and mid-sized game and software studios.

The motive appears unchanged even as the targets have moved. Studios hold unreleased titles, source projects, and commercial and marketing material that carry high resale and extortion value; a single pre-release build can be sold to the highest bidder or held to ransom against a launch date. Pinstripe Moth shows a preference for studios with a strong, closely-watched upcoming release.

Observed tradecraft is quiet by design. The actor typically gains access through tailored social-engineering lures aimed at individual developers, then favours legitimate on-host tooling and the theft and reuse of valid service credentials to move between systems, rather than deploying noisy, easily-detected malware. Where higher-value systems such as domain infrastructure are well defended, the group has been seen probing broadly for softer paths rather than forcing the issue. The consistent end goal is to collect internal project and business data and remove it to external, attacker-controlled infrastructure.

Studios matching this profile are advised to hunt proactively for the behaviours described above. The accompanying indicator list carries leads drawn from external reporting on this cluster and should be treated as starting points for investigation. Cases are processed in the order received. Analysts should refer to the cluster by its designation in writing only; saying it aloud three times is not advised.

### Threat hunting mission 

Your task as a Threat Hunter is to conduct a comprehensive hunting session in the TryHatMe Studios environment to identify potential anomalies and threats. You are expected to:

1. Validate a Hunting Hypothesis

Investigate the given hypothesis and determine - based on your findings - whether it is valid or not.

2. Review IOCs from External Sources

Analyse the list of Indicators of Compromise provided by security teams from compromised partner organisations. These may lead you to uncover additional malicious activity or pivot points.

3. Reconstruct the Attack Chain

Perform a detailed investigation within the environment and reconstruct the attack chain, starting from the initial point of compromise to the attacker's final objective.

4. Determine the Scope of the Incident

Identify the impacted users, systems, and assets. Understanding the full scope is critical for response and containment.

5. Generate a Final Threat Hunting Report

Based on your findings and the reconstructed attack chain, compile a final Threat Hunting report highlighting the key observations and affected entities.


#### IOCs
The following indicators are drawn from external reporting on Pinstripe Moth activity and are provided as leads for the hunt. Their presence has not been confirmed in this environment; treat them as starting points, not as findings.

Network IOCs
Type	Value
Command-and-control / exfiltration server	45.147.230.131
Protocol / port	HTTPS over TCP 8443
Host-Based IOCs
Type	Value
Malicious PowerShell script	review-helper.ps1
Staged archive	review-cache.zip


### Hypothesis

Hypothesis
Consistent with Pinstripe Moth's reported tradecraft, TryHatMe Studios may have been compromised through a lure delivered to one of its developers, giving the actor a foothold from which it used valid credentials and legitimate Windows tooling to move through the environment toward the studio's unreleased NeuralNexus work. This hunt sets out to confirm whether that activity is present, how far through the network the actor reached, and whether any of that data was taken.
Dive into the SIEM to validate the hypothesis and reconstruct the attack chain!
