# SilentDividend — challenge notes and walkthroughs

This section documents the analysis of the `SilentDividend` challenge from Holmes CTF 2026. The emphasis is not only on recovering the answers, but on understanding the tradecraft used by the malicious package: Electron preload abuse, file staging, Windows API telemetry, blockchain-backed payloads, and wallet approval manipulation.

## Challenge intent

The challenge simulates a malicious desktop application that:

- stages files into a public writable directory,
- executes a PowerShell bypass,
- launches a Lua script that touches filesystem activity,
- reaches out to a remote HTTP endpoint,
- reads a value from an Ethereum smart contract,
- decrypts embedded payloads,
- and presents a UI built to trick the user into approving token spend.

This is a realistic SOC / DFIR / threat hunting exercise because it combines:

- Windows internals and API behavior,
- application triage,
- blockchain contract analysis,
- static review of Electron `preload.js`,
- UI layer deception analysis,
- and evidence reconstruction across multiple layers.

## Folder layout

- `artifacts/` — original challenge artifacts and extracted files
- `answers/` — fully explained walkthroughs for all 10 questions, in English
- `Dockerfile` — minimal container build used to run the decryption logic when Node is unavailable locally
- `flag.js` — challenge reproduction script used to recover the contract-backed payload

## Questions covered

1. Copy location of extracted files
2. Structure describing directory change notifications
3. Win32 API used for HTTP request
4. Smart contract function used for decryption key retrieval
5. Recovered hidden payload from encrypted data
6. Temporary directory variable used for HTML launch
7. Token function used to request spending approval
8. Exact token amount passed in the approval call
9. Ethers provider class used for wallet connection
10. HTML contract reference and hidden coordinate recovery

## Learning outcomes

This challenge maps cleanly to real SOC skill areas:

- Threat hunting against deceptive desktop software
- File staging and persistence concepts
- PowerShell abuse and bypass techniques
- Windows API reconnaissance and event-driven file monitoring
- Blockchain contract interaction via RPC and ABI inspection
- Smart contract logic analysis and hidden-data recovery
- Recognizing wallet-drainer UX patterns in browser/Electron UIs

## Start here

Use the answers index in [answers/README.md](answers/README.md) to navigate all question walkthroughs.

## Answers summary

- 1 — `C:\Users\Public`
- 2 — `FILE_NOTIFY_INFORMATION`
- 3 — `WinHttpSendRequest`
- 4 — `resolveState()`
- 5 — `AUTH=NAPOLEON SETTLEMENT_REFERENCE=SR-4821`
- 6 — `%TEMP%`
- 7 — `approve()`
- 8 — `115792089237316195423570985008687907853269984665640564039457584007913129639935`
- 9 — `BrowserProvider`
- 10 — `51.5049,0.0348`

---

This challenge is best understood as a layered forensic case: the UI is a decoy, the `preload.js` is the real loader, and the smart contract is the hidden source of truth.
