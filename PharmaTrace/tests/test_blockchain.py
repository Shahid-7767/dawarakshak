from blockchain.chain import Blockchain

def test_genesis_chain_is_valid():
    chain = Blockchain()
    assert len(chain.blocks) == 1
    assert chain.is_valid()

def test_three_of_four_approvals_commit():
    chain = Blockchain()
    result = chain.add_transaction({"type": "TEST"}, [True, True, True, False])
    assert result["accepted"] is True
    assert len(chain.blocks) == 2
    assert chain.is_valid()

def test_two_of_four_approvals_reject():
    chain = Blockchain()
    result = chain.add_transaction({"type": "TEST"}, [True, True, False, False])
    assert result["accepted"] is False
    assert len(chain.blocks) == 1

def test_tampering_is_detected():
    chain = Blockchain()
    chain.add_transaction({"type": "TEST"})
    chain.blocks[1].transactions[0]["type"] = "ALTERED"
    assert chain.is_valid() is False
