# Q9 — Which ethers provider class is used for the wallet connection?

## Question

What ethers.js v6 provider class is used to connect to the browser wallet?

## Why this matters

This helps connect the front-end logic to the wallet in the browser and is a common API used in dApps. Understanding the provider class is important because it defines how the app interacts with MetaMask or a browser wallet.

## Key evidence

The page contains:

```js
provider = new ethers.BrowserProvider(window.ethereum);
await provider.send("eth_requestAccounts", []);
signer = await provider.getSigner();
```

Therefore the provider class is:

```text
BrowserProvider
```

## SOC interpretation

This reveals that the UI is designed to prompt the user for wallet access and then request a signature or approval. In real SOC investigations, this is a strong signal of a web3-driven malicious interface.

## Final answer

```text
BrowserProvider
```

## Summary

The app uses the ethers v6 browser wallet provider to request wallet access and then interacts with the connected signer. This is a standard Web3 UI flow that is often abused in wallet-draining front ends.
