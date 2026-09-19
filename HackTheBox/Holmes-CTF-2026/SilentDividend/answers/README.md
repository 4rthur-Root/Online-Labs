# SilentDividend answers index

This folder contains the 10 question-by-question walkthroughs for the SilentDividend challenge. Each walkthrough focuses on the actual reasoning path, the SOC mapping, the technical detail, and the final answer.

## Index

1. [01-copy-location-extraresources.md](01-copy-location-extraresources.md)
2. [02-file-notify-information.md](02-file-notify-information.md)
3. [03-winhttpsendrequest.md](03-winhttpsendrequest.md)
4. [04-resolve-state.md](04-resolve-state.md)
5. [05-contract-decryption-payload.md](05-contract-decryption-payload.md)
6. [06-temp-directory.md](06-temp-directory.md)
7. [07-approve-function.md](07-approve-function.md)
8. [08-maxuint256-amount.md](08-maxuint256-amount.md)
9. [09-browser-provider.md](09-browser-provider.md)
10. [10-html-smart-contract-coordinate.md](10-html-smart-contract-coordinate.md)

## SOC mapping

This challenge aligns to the following SOC and digital forensics competencies:

- endpoint triage and malicious app analysis
- dynamic/static identification of staged persistence and loading techniques
- API-level interpretation of Windows file events
- HTTP client behavior analysis
- blockchain and smart contract triage
- identifying deceptive UX flows and wallet-approval phishing
- reconstructing hidden artifacts and encoded values

## Reading pattern

Each file follows the same structure:

- Question
- Why it matters in a real SOC investigation
- Technical investigation steps
- Key findings
- Final answer
- Summary / learning points

## Final answer set

- Q1: `C:\Users\Public`
- Q2: `FILE_NOTIFY_INFORMATION`
- Q3: `WinHttpSendRequest`
- Q4: `resolveState()`
- Q5: `AUTH=NAPOLEON SETTLEMENT_REFERENCE=SR-4821`
- Q6: `%TEMP%`
- Q7: `approve()`
- Q8: `115792089237316195423570985008687907853269984665640564039457584007913129639935`
- Q9: `BrowserProvider`
- Q10: `51.5049,0.0348`
