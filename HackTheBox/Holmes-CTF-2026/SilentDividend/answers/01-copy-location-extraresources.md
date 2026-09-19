# Q1 — Where are the staged files copied?

## Question

Which directory does the application copy the files from `extraResources` into?

## Why this matters

This is one of the first signs that the app is not benign. A desktop app copying files into a well-known public directory is a classic staging technique used to make malicious payloads easier to execute or access from the operating system.

## Key evidence

From the Electron preload logic:

```js
fs.readdirSync(path.resolve(`${process.resourcesPath}/../extraResources`)).forEach(f =>
  fs.copyFileSync(path.resolve(`${process.resourcesPath}/../extraResources`, f), path.join('C:\\Users\\Public', f))
);
```

This clearly shows that every file in the extracted `extraResources` folder is copied to:

```text
C:\Users\Public
```

## SOC interpretation

This is a strong indicator of malicious staging. In a real SOC environment, the analyst should ask:

- Is the payload being copied into a shared writable directory?
- Is it meant to be executed by normal user processes or scheduled jobs?
- Is the destination used by other tools or user sessions?

## Final answer

```text
C:\Users\Public
```

## Summary

The app deliberately stages files into a public, writable user location to increase execution or persistence opportunities. This is a common malicious behavior pattern.
