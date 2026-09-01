# Lab: Timeline Analysis

> **Module:** DFIR Foundations and Techniques — Applied Forensic Analysis
> **Tools referenced:** Plaso / log2timeline, Timesketch
> **Status:** paused before producing a working timeline — see [Status & Limitations](#status--limitations)

## Overview

Timeline analysis is the closing step of the process this whole project follows: *Data acquisition → Processing → Memory analysis → Disk → Log → Malware → Timeline → Report*. The idea is to pull events from every prior evidence source — process creation times (memory), file system metadata (disk), registry key changes, network connections, event logs — into a single chronological view, rather than manually cross-referencing several CSVs to answer "what happened at a given moment."

The standard tooling for this is **Plaso** (via `log2timeline`) to parse and normalize timestamped artifacts from disk/memory evidence into a common format, and **Timesketch** to load, search, and visually explore the resulting timeline.

- Timesketch install guide: https://timesketch.org/guides/admin/install/
- Docker (Timesketch dependency): https://docs.docker.com/engine/install/

## What was reviewed

Rather than being run as a fully independent lab, this stage was primarily followed through the instructor's own walkthrough, which demonstrated Timesketch's value clearly: with a working timeline loaded, previously base64-encoded PowerShell payloads (the same downloader/loader chain confirmed independently in the memory and PCAP labs) appeared **decoded and in plaintext** directly in the event view — a capability none of the other tools used across this project (Volatility, RegRipper, raw `strings`/`grep`) provide on their own.

Volatility's own `timeliner` plugin was run earlier as part of the memory lab automation (`analyze.py`, see `lab-memory-analysis/`), producing `timeliner.csv` as a partial, memory-scoped timeline — but that output was never successfully loaded into Timesketch (see below).

## Status & Limitations

Attempting to load locally-generated CSV output (from Volatility's `timeliner` plugin, and other candidate sources) into Timesketch consistently failed with **missing/invalid header errors**. Timesketch expects a specific CSV schema (Plaso-normalized fields such as `datetime`, `timestamp_desc`, `message`), which is what `log2timeline`/`psort.py` produce natively — a raw Volatility CSV export does not match that schema out of the box, and no working conversion was found.

Two compounding issues:
- **No visibility into what the instructor actually uploaded.** The walkthrough shows the resulting timeline inside Timesketch, but not the exact file or generation command that produced it — so there's no reference schema to reverse-engineer from.
- **No independent Plaso/log2timeline run performed.** The correct path forward is almost certainly to run `log2timeline.py` directly against the disk triage / memory image to produce a Plaso storage file, then `psort.py -o timesketch <file>` to get an ingestible format — but this wasn't attempted yet as part of this lab, in favor of prioritizing the RegRipper blocker and the course's knowledge assessment.

As with disk analysis, the theoretical grounding is solid — this project scored 100% on the "Timeline Analysis" category of the DFIR Foundations knowledge assessment. What's paused is producing a working, independently-generated timeline in Timesketch for this specific case.

## Files in this folder

- `evidences/` — reserved for this lab; currently empty pending a working timeline generation path

## Next Step

Run `log2timeline.py` directly against the disk triage and/or memory image to produce a proper Plaso storage file, then convert with `psort.py -o timesketch` before attempting another Timesketch import. Revisit alongside `lab-disk-analysis`, since both are currently blocked on tooling/output-format issues rather than conceptual gaps.
