# Q6 — Which environment variable points to the HTML destination directory?

## Question

Which environment variable corresponds to the directory where the application copies the HTML file from its package?

## Why this matters

This is a quick but important clue about how the malicious app reuses the local temp context to stage and launch a foothold file. The environment variable identifies the write-and-launch location.

## Key evidence

The decoded payload contains:

```text
start "" "%TEMP%\settlement.html"
```

That means the package artifact is written to and launched from the Windows temp folder, which is defined by:

```text
%TEMP%
```

## SOC interpretation

This is a common artifact pattern in malicious desktop applications: moving a locally embedded file into a temp directory and launching it from there to make it appear benign or less obvious to the user.

## Final answer

```text
%TEMP%
```

## Summary

The HTML file is not launched from the app bundle directly; it is copied into the temp directory and then opened from there. `%TEMP%` is the relevant environment variable.
