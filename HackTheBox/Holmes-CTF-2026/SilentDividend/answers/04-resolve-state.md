# Q4 — Which smart contract method is used to fetch the key?

## Question

Which smart contract function does the Electron application call to retrieve the decryption key for the encrypted payload?

## Why this matters

This is the bridge between the desktop application and the blockchain. It shows that the payload is not just stored locally; it is hidden behind a remote on-chain value that the app pulls dynamically.

## Key evidence

In the preload logic:

```js
const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    CONTRACT_ABI,
    provider
);

const state = await contract.resolveState();
```

The ABI is:

```js
const CONTRACT_ABI = [
    'function resolveState() view returns (bytes32)'
];
```

So the function is clearly:

```text
resolveState()
```

## SOC interpretation

This is important because the malicious app is doing a data fetch from the blockchain instead of relying only on local files. In a real SOC engagement, this means:

- there is a remote or on-chain control plane,
- the app is not fully self-contained,
- the encryption key is dynamic and may change depending on the chain state,
- and blockchain inspection becomes part of threat hunting.

## Final answer

```text
resolveState()
```

## Summary

The application uses a read-only contract function to retrieve a `bytes32` state key. That key is then used to decode the embedded payload, making the blockchain a part of the malicious logic chain.
