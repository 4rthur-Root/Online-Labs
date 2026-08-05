# Security Operations in Enterprise Environments

> **Module:** Part 2 – Elevate Your DFIR Skills
> **Topics covered:** 7 (per course outline)

## Overview

This module shifts from the general DFIR/forensics foundation built in Part 1 toward the operational side of security: how SOC teams organize their work, what capabilities they rely on, and how a real investigation actually unfolds once evidence is in hand. It closes with a hands-on lab applying these ideas directly to network evidence from Alice's compromised workstation.

## Topics

1. **Introduction**
2. **SOC Core Capabilities**
3. **Threat Intelligence & Threat Hunting**
4. **Incident Handling**
5. **Case Introduction** — sets up the Alice compromise scenario used throughout Part 2
6. **Lab: PCAP Analysis** — hands-on investigation, documented in [`lab-pcap-analysis/`](lab-pcap-analysis/)
7. **Session Resources**

## Lab

The practical component of this module is a full investigation of `traffic.pcapng`, reconstructing a multi-stage attack chain — DNS typosquatting, HTA-based delivery, PowerShell payload decoding, and confirmed C2 beaconing — entirely from packet capture evidence.

➡️ [Full writeup: Lab - PCAP Analysis](lab-pcap-analysis/README.md)

## Key takeaway

The case study reinforces a theme carried over from Part 1: effective SOC work isn't just running tools, it's building a coherent narrative from fragmented evidence. Each artifact (a DNS query, an HTTP header, a Base64 blob) means little in isolation — the value is in connecting them into a timeline that explains *what happened* and *what would have stopped it*.
