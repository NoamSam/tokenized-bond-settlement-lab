// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

/// @title DvPSettlement
/// @notice Atomic Delivery-versus-Payment settlement of a tokenized bond
///         against a stablecoin. Both legs settle in a single transaction:
///         either the investor pays AND receives the bonds, or the whole
///         transaction reverts. This removes principal risk, which is the
///         core promise of DvP (BIS settlement model 1).
/// @dev    Both parties must approve this contract beforehand:
///         - investor approves the cash token for `cashAmount`
///         - issuer approves the bond token for `bondAmount`
contract DvPSettlement {
    using SafeERC20 for IERC20;

    event SettlementExecuted(
        uint256 indexed orderId,
        address indexed investor,
        address indexed issuer,
        address bondToken,
        uint256 bondAmount,
        address cashToken,
        uint256 cashAmount
    );

    error NotAParty();
    error AlreadySettled(uint256 orderId);

    /// @notice Order ids already settled, to keep the off-chain order book
    ///         and on-chain settlement in sync (one settlement per order).
    mapping(uint256 => bool) public settled;

    /// @param orderId    Off-chain BondOrder id (backend primary key).
    /// @param investor   Buyer: pays cash, receives bonds.
    /// @param issuer     Seller: delivers bonds, receives cash.
    function settle(
        uint256 orderId,
        address investor,
        address issuer,
        IERC20 bondToken,
        uint256 bondAmount,
        IERC20 cashToken,
        uint256 cashAmount
    ) external {
        if (msg.sender != investor && msg.sender != issuer) revert NotAParty();
        if (settled[orderId]) revert AlreadySettled(orderId);
        settled[orderId] = true;

        // Cash leg: investor -> issuer
        cashToken.safeTransferFrom(investor, issuer, cashAmount);
        // Delivery leg: issuer -> investor
        bondToken.safeTransferFrom(issuer, investor, bondAmount);

        emit SettlementExecuted(
            orderId,
            investor,
            issuer,
            address(bondToken),
            bondAmount,
            address(cashToken),
            cashAmount
        );
    }
}
