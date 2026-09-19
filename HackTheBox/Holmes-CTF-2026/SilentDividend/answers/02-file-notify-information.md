# Q2 — Which Win32 structure describes the directory-change buffer?

## Question

Which Win32 structure defines the format of the buffer returned by the Lua script when monitoring directory changes?

## Why this matters

This is the point where the analysis starts to move from general app behavior to low-level Windows filesystem monitoring. It is a very common artifact in malware and persistence research.

## Key evidence

The relevant Windows structure is:

```cpp
typedef struct _FILE_NOTIFY_INFORMATION {
  DWORD NextEntryOffset;
  DWORD Action;
  DWORD FileNameLength;
  WCHAR FileName[1];
} FILE_NOTIFY_INFORMATION, *PFILE_NOTIFY_INFORMATION;
```

This structure is returned by APIs such as `ReadDirectoryChangesW`, which are used to monitor directory activity and receive change records in batches.

## SOC interpretation

This matters because a directory watcher can reveal:

- creation or deletion of payloads,
- writes to user- or temp-controlled folders,
- suspicious activity in application paths or profile directories,
- logic that reacts to file changes.

In a SOC context, this often indicates a process that is waiting for a file launch or a manipulation to trigger execution.

## Final answer

```text
FILE_NOTIFY_INFORMATION
```

## Summary

The Lua script is likely monitoring filesystem events via `ReadDirectoryChangesW`. The structure used to decode the event buffer is `FILE_NOTIFY_INFORMATION`, which is the canonical Windows format for directory change notifications.
