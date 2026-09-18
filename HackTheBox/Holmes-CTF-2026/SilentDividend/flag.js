const { ethers } = require("ethers");

const RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com";
const CONTRACT_ADDRESS = "0xbB63Ae28E4f75C9392bae69cDf5394Ca0ACdA6B1";

const ENCRYPTED_DATA =
  "0x560c325bdd0aeea2cd2690a2ed1c1b4a28deca7ac2a40ce8d2725d539a950ca8f4a4bcf375806c36532258a0cf16c19c12989e0aa0e25a72be241da7d2f74cfa2c4c4e1bbfc6204207fe5c801d201f5af84864f0";

function decryptEmbeddedData(encryptedData, encryptionKey) {
  const data = Buffer.from(encryptedData.slice(2), "hex");
  const key = Buffer.from(encryptionKey.slice(2), "hex");
  const result = Buffer.alloc(data.length);

  for (let i = 0; i < data.length; i++) {
    const step1 = data[i] ^ key[i % key.length];

    const step2 =
      ((step1 << 7) | (step1 >>> 1)) & 0xff;

    result[i] = step2 ^ 0x42;
  }

  return result.toString("utf8");
}

async function main() {
  const provider = new ethers.JsonRpcProvider(RPC_URL);

  const contract = new ethers.Contract(
    CONTRACT_ADDRESS,
    ["function resolveState() view returns (bytes32)"],
    provider
  );

  const state = await contract.resolveState();

  console.log("Clé récupérée :", state);
  console.log("Valeur déchiffrée :");
  console.log(decryptEmbeddedData(ENCRYPTED_DATA, state));
}

main().catch(console.error);