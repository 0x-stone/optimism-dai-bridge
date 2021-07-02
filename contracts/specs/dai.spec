// dai.spec
// Verify that supply and balance hold on mint
rule mint(uint256 wad) {
    // The env type represents the EVM parameters passed in every
    //   call (msg.*, tx.*, block.* variables in solidity).
    env e;

    // Save the totalSupply and sender balance before minting
    uint256 supplyBefore = totalSupply(e);
    uint256 senderBalance = balanceOf(e, e.msg.sender);

    mint(e, e.msg.sender, wad);

    uint256 supplyAfter = totalSupply(e);

    assert(balanceOf(e, e.msg.sender) == senderBalance + wad, "Mint did not increase the balance as expected");
    assert(supplyBefore + wad == supplyAfter, "Mint did not increase the supply as expected");
}

// Verify that supply and balance hold on burn
rule burn(uint256 wad) {
     env e;

    require balanceOf(e, e.msg.sender) > 0;

    uint256 supplyBefore = totalSupply(e);
    uint256 senderBalance = balanceOf(e, e.msg.sender);

    burn(e, e.msg.sender, wad);

    assert(balanceOf(e, e.msg.sender) == senderBalance - wad, "Burn did not decrease the balance as expected");
    assert(totalSupply(e) == supplyBefore - wad, "Burn did not decrease the supply as expected");
}

// Verify that balance hold on transfer
rule transfer(uint256 wad) {
    env e;

    address alice;

    require e.msg.sender != alice;
    require balanceOf(e, e.msg.sender) >= wad;

    uint256 senderBalance = balanceOf(e, e.msg.sender);
    uint256 aliceBalance = balanceOf(e, alice);

    require aliceBalance + wad <= max_uint; // assuming not overflow in practise

    transfer(e, alice, wad);

    assert(balanceOf(e, e.msg.sender) == senderBalance - wad, "Transfer did not decrease the balance as expected");
    assert(balanceOf(e, alice) == aliceBalance + wad, "Transfer did not increase the balance as expected");
}

// Verify that balance hold on transferFrom
rule transferFrom(uint256 wad) {
    env e;

    address alice;

    require e.msg.sender != alice;
    require balanceOf(e, e.msg.sender) >= wad;

    uint256 senderBalance = balanceOf(e, e.msg.sender);
    uint256 aliceBalance = balanceOf(e, alice);

    require aliceBalance + wad <= max_uint; // assuming not overflow in practise

    transferFrom(e, e.msg.sender, alice, wad);

    assert(balanceOf(e, e.msg.sender) == senderBalance - wad, "TransferFrom did not decrease the balance as expected");
    assert(balanceOf(e, alice) == aliceBalance + wad, "TransferFrom did not increase the balance as expected");
}
