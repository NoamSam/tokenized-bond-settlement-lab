/**
 * End-to-end demo: deploys the contracts on the in-process Hardhat network,
 * funds the investor, executes an atomic DvP settlement, and prints a JSON
 * payload ready to be recorded in the Django backend:
 *
 *   npx hardhat run scripts/settle-demo.js
 *   cd ../backend && python manage.py record_onchain_settlement \
 *       --order-id 1 --tx-hash 0x... --block-number N
 */
const { ethers } = require("hardhat");

async function main() {
  const ORDER_ID = 1;
  const BOND_AMOUNT = 2n;
  const CASH_AMOUNT = 200000n; // 2000.00 FAKEUR in cents

  const [issuer, investor] = await ethers.getSigners();

  const bond = await ethers.deployContract("BondToken", [
    "Tokenized EUR Bond 2027",
    "BOND2027",
    1000n,
    issuer.address,
  ]);
  const cash = await ethers.deployContract("FakeEuroStablecoin");
  const dvp = await ethers.deployContract("DvPSettlement");

  await cash.mint(investor.address, CASH_AMOUNT);
  await cash.connect(investor).approve(await dvp.getAddress(), CASH_AMOUNT);
  await bond.connect(issuer).approve(await dvp.getAddress(), BOND_AMOUNT);

  const tx = await dvp
    .connect(investor)
    .settle(
      ORDER_ID,
      investor.address,
      issuer.address,
      bond,
      BOND_AMOUNT,
      cash,
      CASH_AMOUNT
    );
  const receipt = await tx.wait();

  console.log(
    JSON.stringify(
      {
        order_id: ORDER_ID,
        chain: "local_ethereum",
        transaction_hash: receipt.hash,
        block_number: receipt.blockNumber,
        gas_used: receipt.gasUsed.toString(),
        investor_bond_balance: (await bond.balanceOf(investor.address)).toString(),
        issuer_cash_balance: (await cash.balanceOf(issuer.address)).toString(),
      },
      null,
      2
    )
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
