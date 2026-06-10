const { expect } = require("chai");
const { loadFixture } = require("@nomicfoundation/hardhat-toolbox/network-helpers");
const { ethers } = require("hardhat");

const ORDER_ID = 1;
const BOND_SUPPLY = 1000n; // 1000 indivisible bond units
const BOND_AMOUNT = 2n; // order: 2 bonds
const CASH_AMOUNT = 200000n; // 2 * 1000.00 EUR in cents (2 decimals)

describe("DvP settlement of a tokenized bond", function () {
  async function deployFixture() {
    const [issuer, investor, stranger] = await ethers.getSigners();

    const bond = await ethers.deployContract("BondToken", [
      "Tokenized EUR Bond 2027",
      "BOND2027",
      BOND_SUPPLY,
      issuer.address,
    ]);
    const cash = await ethers.deployContract("FakeEuroStablecoin");
    const dvp = await ethers.deployContract("DvPSettlement");

    // Fund the investor with demo cash
    await cash.mint(investor.address, CASH_AMOUNT);

    return { bond, cash, dvp, issuer, investor, stranger };
  }

  async function approvedFixture() {
    const ctx = await deployFixture();
    const { bond, cash, dvp, issuer, investor } = ctx;
    await cash.connect(investor).approve(await dvp.getAddress(), CASH_AMOUNT);
    await bond.connect(issuer).approve(await dvp.getAddress(), BOND_AMOUNT);
    return ctx;
  }

  function settle(ctx, caller) {
    const { bond, cash, dvp, issuer, investor } = ctx;
    return dvp
      .connect(caller)
      .settle(
        ORDER_ID,
        investor.address,
        issuer.address,
        bond,
        BOND_AMOUNT,
        cash,
        CASH_AMOUNT
      );
  }

  describe("deployment", function () {
    it("mints the full bond supply to the issuer with 0 decimals", async function () {
      const { bond, issuer } = await loadFixture(deployFixture);
      expect(await bond.decimals()).to.equal(0);
      expect(await bond.balanceOf(issuer.address)).to.equal(BOND_SUPPLY);
    });

    it("uses 2 decimals for the euro stablecoin", async function () {
      const { cash } = await loadFixture(deployFixture);
      expect(await cash.decimals()).to.equal(2);
    });
  });

  describe("happy path", function () {
    it("atomically swaps cash and bonds", async function () {
      const ctx = await loadFixture(approvedFixture);
      const { bond, cash, issuer, investor } = ctx;

      await settle(ctx, investor);

      expect(await bond.balanceOf(investor.address)).to.equal(BOND_AMOUNT);
      expect(await bond.balanceOf(issuer.address)).to.equal(
        BOND_SUPPLY - BOND_AMOUNT
      );
      expect(await cash.balanceOf(issuer.address)).to.equal(CASH_AMOUNT);
      expect(await cash.balanceOf(investor.address)).to.equal(0n);
    });

    it("emits SettlementExecuted with the off-chain order id", async function () {
      const ctx = await loadFixture(approvedFixture);
      const { bond, cash, dvp, issuer, investor } = ctx;

      await expect(settle(ctx, investor))
        .to.emit(dvp, "SettlementExecuted")
        .withArgs(
          ORDER_ID,
          investor.address,
          issuer.address,
          await bond.getAddress(),
          BOND_AMOUNT,
          await cash.getAddress(),
          CASH_AMOUNT
        );
    });

    it("can be triggered by the issuer as well", async function () {
      const ctx = await loadFixture(approvedFixture);
      await expect(settle(ctx, ctx.issuer)).to.not.be.reverted;
    });
  });

  describe("atomicity and safety", function () {
    it("reverts the whole settlement if the cash leg is not approved", async function () {
      const ctx = await loadFixture(deployFixture);
      const { bond, dvp, issuer, investor } = ctx;
      // Only the bond leg is approved
      await bond.connect(issuer).approve(await dvp.getAddress(), BOND_AMOUNT);

      await expect(settle(ctx, investor)).to.be.reverted;
      expect(await bond.balanceOf(investor.address)).to.equal(0n);
    });

    it("reverts the whole settlement if the delivery leg is not approved", async function () {
      const ctx = await loadFixture(deployFixture);
      const { cash, dvp, investor, issuer } = ctx;
      // Only the cash leg is approved
      await cash.connect(investor).approve(await dvp.getAddress(), CASH_AMOUNT);

      await expect(settle(ctx, investor)).to.be.reverted;
      expect(await cash.balanceOf(issuer.address)).to.equal(0n);
    });

    it("rejects a caller that is not a party to the trade", async function () {
      const ctx = await loadFixture(approvedFixture);
      await expect(settle(ctx, ctx.stranger)).to.be.revertedWithCustomError(
        ctx.dvp,
        "NotAParty"
      );
    });

    it("rejects settling the same order id twice", async function () {
      const ctx = await loadFixture(approvedFixture);
      const { bond, cash, dvp, issuer, investor } = ctx;
      await settle(ctx, investor);

      // Re-approve and retry with the same order id
      await cash.mint(investor.address, CASH_AMOUNT);
      await cash.connect(investor).approve(await dvp.getAddress(), CASH_AMOUNT);
      await bond.connect(issuer).approve(await dvp.getAddress(), BOND_AMOUNT);

      await expect(settle(ctx, investor)).to.be.revertedWithCustomError(
        dvp,
        "AlreadySettled"
      );
    });
  });
});
