# Q8 — What exact amount is approved?

## Question

What is the exact token amount passed to the approval call?

## Why this matters

The approval amount is crucial because it determines the danger level. A value equal to the maximum `uint256` means the spender can drain the victim’s tokens without further approval.

## Key evidence

The page contains:

```js
const unlimitedAmount = ethers.MaxUint256;
```

Then:

```js
const tx = await token.approve(X0_CONTRACT_ADDRESS, unlimitedAmount);
```

`ethers.MaxUint256` maps to the maximum value of a uint256:

```text
115792089237316195423570985008687907853269984665640564039457584007913129639935
```

## SOC interpretation

This is a strong indicator of an approval-granting drainer. Granting `MaxUint256` means the spender can spend arbitrarily large amounts, making the approval effectively unlimited.

## Final answer

```text
115792089237316195423570985008687907853269984665640564039457584007913129639935
```

## Summary

The wallet approval is intentionally set to the maximum possible token allowance. That is the key behavioral sign of a dangerous Web3 approval flow.
