# Q5 — Recover the hidden payload from the encrypted data

## Question

Investigate the smart contract using its address, analyze its logic, and recover the hidden flag by decoding the encrypted data.

## Why this matters

This question combines three important analyst skills:

- blockchain contract inspection,
- decryption logic reconstruction,
- and payload recovery from embedded artifacts.

It is a typical pattern in malicious desktop applications: dynamic key retrieval + embedded encrypted string + execution of decoded command.

## Key evidence

The preload contains:

```js
const CONTRACT_ADDRESS = '0xbB63Ae28E4f75C9392bae69cDf5394Ca0ACdA6B1';

const ENCRYPTED_DATA =
  '0x560c325bdd0aeea2cd2690a2ed1c1b4a28deca7ac2a40ce8d2725d539a950ca8f4a4bcf375806c36532258a0cf16c19c12989e0aa0e25a72be241da7d2f74cfa2c4c4e1bbfc6204207fe5c801d201f5af84864f0';
```

And the decryption flow is:

```js
const state = await contract.resolveState();
const decrypted = decryptEmbeddedData(ENCRYPTED_DATA, state);
```

The custom decryption algorithm is:

```js
const step1 = data[i] ^ keyByte;
const step2 = ((step1 << 7) | (step1 >>> 1)) & 0xff;
result[i] = step2 ^ 0x42;
```

## Reconstructed result

When the key is retrieved from the contract, the final decoded string is:

```text
start "" "%TEMP%\settlement.html" && echo AUTH=NAPOLEON SETTLEMENT_REFERENCE=SR-4821
```

This reveals the key output values:

```text
AUTH=NAPOLEON
SETTLEMENT_REFERENCE=SR-4821
```

## SOC interpretation

This is valuable because it shows how a malicious app can:

- fetch a dynamic key from a blockchain,
- keep the payload obfuscated in code,
- and execute a command after revealing the real content.

This is important for both malware hunting and detection engineering: never assume the payload is stored in plain text if a contract or dynamic key is involved.

## Final answer

```text
AUTH=NAPOLEON SETTLEMENT_REFERENCE=SR-4821
```

## Summary

The contract-backed key is the true decryption primitive. Once decoded, the hidden payload is not a simple string but a Windows command that opens a local HTML page and prints operational values.
