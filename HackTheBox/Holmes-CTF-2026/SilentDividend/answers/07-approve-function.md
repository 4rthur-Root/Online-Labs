# Q7 — Which token function is used for approval?

## Question

What token function does the HTML page call to request spending permission?

## Why this matters

This is the precise moment where the UI is trying to get the user to authorize a token approval. In Web3 abuse cases, this usually indicates the front-end is attempting to trigger a spender allowance rather than a direct transfer.

## Key evidence

The page contains:

```js
const tx = await token.approve(X0_CONTRACT_ADDRESS, unlimitedAmount);
```

This is the standard ERC-20 function:

```solidity
approve(address spender, uint256 amount)
```

## SOC interpretation

This is a critical UX-surfacing misuse pattern. The app is not asking the user to sign a transaction to move funds directly; it is asking to approve a spender to pull tokens on behalf of the victim. In real-world cases, that is a classic wallet-drainer flow.

## Final answer

```text
approve()
```

## Summary

The HTML front end is using an ERC-20 approval call, which is exactly the type of flow abused in wallet-draining or on-chain token theft patterns.
