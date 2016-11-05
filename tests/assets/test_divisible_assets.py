import pytest


# CREATE divisible asset
# Single input
# Single owners_before
# Single output
# single owners_after
def test_single_in_single_own_single_out_single_own_create(b, user_vk):
    from bigchaindb.models import Transaction
    from bigchaindb.common.transaction import Asset

    asset = Asset(divisible=True)
    tx = Transaction.create([b.me], [([user_vk], 100)], asset=asset)
    tx_signed = tx.sign([b.me_private])

    assert tx_signed.validate(b) == tx_signed
    assert len(tx_signed.conditions) == 1
    assert tx_signed.conditions[0].amount == 100
    assert len(tx_signed.fulfillments) == 1


# CREATE divisible asset
# Single input
# Single onwers_before
# Multiple outputs
# Single owners_after per output
def test_single_in_single_own_multiple_out_single_own_create(b, user_vk):
    from bigchaindb.models import Transaction
    from bigchaindb.common.transaction import Asset

    asset = Asset(divisible=True)
    tx = Transaction.create([b.me], [([user_vk], 50), ([user_vk], 50)], asset=asset)
    tx_signed = tx.sign([b.me_private])

    assert tx_signed.validate(b) == tx_signed
    assert len(tx_signed.conditions) == 2
    assert tx_signed.conditions[0].amount == 50
    assert tx_signed.conditions[1].amount == 50
    assert len(tx_signed.fulfillments) == 1


# CREATE divisible asset
# Single input
# Single owners_before
# Single output
# Multiple owners_after
def test_single_in_single_own_single_out_multiple_own_create(b, user_vk):
    from bigchaindb.models import Transaction
    from bigchaindb.common.transaction import Asset

    asset = Asset(divisible=True)
    tx = Transaction.create([b.me], [([user_vk, user_vk], 100)], asset=asset)
    tx_signed = tx.sign([b.me_private])

    assert tx_signed.validate(b) == tx_signed
    assert len(tx_signed.conditions) == 1
    assert tx_signed.conditions[0].amount == 100

    condition = tx_signed.conditions[0].to_dict()
    assert 'subfulfillments' in condition['condition']['details']
    assert len(condition['condition']['details']['subfulfillments']) == 2

    assert len(tx_signed.fulfillments) == 1


# CREATE divisible asset
# Single input
# Single owners_before
# Multiple outputs
# Mix: one output with a single owners_after, one output with multiple
#      owners_after
def test_single_in_single_own_multiple_out_mix_own_create(b, user_vk):
    from bigchaindb.models import Transaction
    from bigchaindb.common.transaction import Asset

    asset = Asset(divisible=True)
    tx = Transaction.create([b.me],
                            [([user_vk], 50), ([user_vk, user_vk], 50)],
                            asset=asset)
    tx_signed = tx.sign([b.me_private])

    assert tx_signed.validate(b) == tx_signed
    assert len(tx_signed.conditions) == 2
    assert tx_signed.conditions[0].amount == 50
    assert tx_signed.conditions[1].amount == 50

    condition_cid1 = tx_signed.conditions[1].to_dict()
    assert 'subfulfillments' in condition_cid1['condition']['details']
    assert len(condition_cid1['condition']['details']['subfulfillments']) == 2

    assert len(tx_signed.fulfillments) == 1


# CREATE divisible asset
# Single input
# Multiple owners_before
# Ouput combinations already tested above
# TODO: Support multiple owners_before in CREATE transactions
@pytest.mark.skip(reason=('CREATE transaction do not support multiple'
                          ' owners_before'))
def test_single_in_multiple_own_single_out_single_own_create(b, user_vk):
    from bigchaindb.models import Transaction
    from bigchaindb.common.transaction import Asset

    asset = Asset(divisible=True)
    tx = Transaction.create([b.me, b.me], [([user_vk], 100)], asset=asset)
    tx_signed = tx.sign([b.me, b.me])
    assert tx_signed.validate(b) == tx_signed
