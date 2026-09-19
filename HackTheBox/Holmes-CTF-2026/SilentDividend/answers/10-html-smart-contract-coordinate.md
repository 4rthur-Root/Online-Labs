# Q10 — Recover the hidden coordinate from the HTML-linked drainer contract

## Question

Analyze the HTML page to uncover a smart contract reference. Investigate the contract’s logic and determine how to interact with it to recover the hidden flag.

## Why this matters

This is the final, important “deception vs truth” lesson of the challenge. The visible HTML is a wallet-approval interface, but the hidden flag is produced through a separate on-chain contract logic. This is exactly the kind of multi-layer trick that a strong SOC analyst must recognize.

## 1. The HTML exposes the drainer contract

The relevant code in the HTML is:

```js
const X0_CONTRACT_ADDRESS = "0x69Bf5b7aBA51C3Ee8bF169aB47479ba95DBF709D";
```

This contract is the visible token spender / drainer target. It is not necessarily the contract that produces the hidden flag. It simply shows the contract that the UI is trying to get a wallet approval for.

## 2. The true logic is hidden in the contract code

The key on-chain logic is:

```solidity
bytes32 private x2 = ...;
bytes32 private x3 = ...;
bytes private x4;

function x7() public view returns (address) {
    return address(uint160(uint256(x2) ^ uint256(x3)));
}

function x8(bytes calldata cipherFlag) external {
    require(x4.length == 0, "already set");
    x4 = cipherFlag;
}

function x9(address x10) external view returns (string memory) {
    require(x10 == x7(), "not quite - keep analyzing");
    bytes memory decrypted = _crypt(x4, x10);
    return string(decrypted);
}
```

This means:

- `x2` and `x3` are hidden values,
- `x7()` reconstructs the secret owner address via XOR,
- `x8()` stores a ciphertext,
- `x9(address)` decrypts it only when the correct address is provided.

## 3. The correct interaction pattern

The right interaction is not “approve the token” but rather:

```js
const provider = new ethers.JsonRpcProvider("https://ethereum-sepolia-rpc.publicnode.com");

const x0 = new ethers.Contract(
  "0x69Bf5b7aBA51C3Ee8bF169aB47479ba95DBF709D",
  [
    "function x7() view returns (address)",
    "function x9(address) view returns (string)"
  ],
  provider
);

const owner = await x0.x7();
const flag = await x0.x9(owner);
console.log(flag);
```

The correct owner is computed by the contract, and only that owner can decrypt the hidden value.

## 4. Final output

The recovered value is:

```text
51.5049,0.0348
```

## SOC mapping

This is a very realistic SOC lesson:

- the visible UI is deceptive,
- the true data source is on-chain logic,
- executable trust should never be inferred from a front-end approval flow alone,
- and contract-view functions are a powerful read-only investigation tool.

## Final answer

```text
51.5049,0.0348
```

## Summary

The artifact is designed to make the analyst focus on the approval flow, but the hidden coordinate is recovered by reading the hidden contract logic and calling the correct view function with the reconstructed owner. This is exactly the sort of multi-layer challenge that requires both application analysis and smart-contract understanding.
