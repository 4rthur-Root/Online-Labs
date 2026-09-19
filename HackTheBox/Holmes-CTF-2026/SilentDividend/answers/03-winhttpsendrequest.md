# Q3 — Which API sends the HTTP request?

## Question

Which Win32 API is used by the Lua script to send a remote HTTP request?

## Why this matters

Malicious or suspicious processes frequently use native HTTP functions to exfiltrate data, fetch additional payloads, or contact a command-and-control endpoint. Identifying the API helps map the behavior to execution patterns.

## Key evidence

The function used is the classic WinHTTP client API:

```text
WinHttpSendRequest
```

This belongs to the WinHTTP API family and is the standard low-level mechanism for sending HTTP/HTTPS requests from Windows native code.

## SOC interpretation

This matters because:

- it suggests a network callback or beaconing behavior,
- the process is not simply reading a local file,
- it actively issues outbound HTTP/S requests,
- and the behavior should be correlated with created files or spawned processes.

## Final answer

```text
WinHttpSendRequest
```

## Summary

The payload uses the WinHTTP stack to send an HTTP request. That is a clear network-beacon indicator and a relevant SOC-hunting artifact.
