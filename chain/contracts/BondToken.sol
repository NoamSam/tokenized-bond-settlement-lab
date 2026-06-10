// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title BondToken
/// @notice ERC-20 representation of a tokenized bond. One token = one bond
///         unit, hence 0 decimals. The full supply is minted to the issuer,
///         which then delivers bonds to investors through DvP settlement.
/// @dev Educational project: a production security token would add transfer
///      restrictions (whitelisting / KYC checks, e.g. ERC-1404 or ERC-3643).
contract BondToken is ERC20 {
    address public immutable issuer;

    constructor(
        string memory name_,
        string memory symbol_,
        uint256 totalSupply_,
        address issuer_
    ) ERC20(name_, symbol_) {
        issuer = issuer_;
        _mint(issuer_, totalSupply_);
    }

    /// @notice Bonds are indivisible units.
    function decimals() public pure override returns (uint8) {
        return 0;
    }
}
