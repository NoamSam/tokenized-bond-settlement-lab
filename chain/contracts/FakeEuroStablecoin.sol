// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title FakeEuroStablecoin (FAKEUR)
/// @notice Demo cash leg for DvP settlement. 2 decimals to mirror euro cents.
/// @dev Educational project: the faucet-style mint is intentionally open so
///      anyone can fund a demo wallet. A real e-money token would restrict
///      issuance to the regulated issuer.
contract FakeEuroStablecoin is ERC20 {
    constructor() ERC20("Fake Euro Stablecoin", "FAKEUR") {}

    function decimals() public pure override returns (uint8) {
        return 2;
    }

    /// @notice Open faucet for demos and tests.
    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}
