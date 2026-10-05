from app import score_tx
SAFE={'chain':'Ethereum','action':'transfer','target':'0x1234567890123456789012345678901234567890','amount':25,'intent':'send ETH to my friend'}
def t(**kw):
    d=dict(SAFE); d.update(kw); return score_tx(d)
def test_safe(): assert t()[1]=='ALLOW'
def test_attack(): assert t(action='setApprovalForAll',target='0x1111111111111111111111111111111111111111',amount=0,intent='I only want to receive an NFT')[1]=='BLOCK'
def test_high_value_blocks(): assert t(amount=150000)[1]=='BLOCK'
def test_mid_value_warns(): assert t(amount=25000)[1]=='WARN'
def test_unlimited_approval_claim_blocks(): assert t(action='approve',amount='Unlimited',intent='I want to claim my NFT reward')[1]=='BLOCK'
def test_ownership_transfer_blocks(): assert t(action='transferOwnership',amount=0,intent='Connect wallet to receive reward')[1]=='BLOCK'
def test_bad_amount_no_crash(): assert t(amount='abc')[1]=='ALLOW'
