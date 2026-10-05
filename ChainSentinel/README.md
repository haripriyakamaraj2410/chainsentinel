# ChainSentinel — Intent-Aware Web3 Transaction Security Firewall

**Hackathon title:** ChainSentinel: Intent-Aware Web3 Transaction Security Firewall

**Pitch:** ChainSentinel checks a Web3 transaction before signing and detects dangerous permissions, suspicious targets, high-value transfers and, most importantly, mismatches between what the user says they intend to do and what the transaction actually grants.

## Stack
Frontend: HTML/CSS/JavaScript | Backend: Flask REST API | Database: SQLite | Detection: explainable weighted rules.

## Run
1. Install Python 3.10+.
2. Open terminal in this folder.
3. `python -m venv .venv`
4. Windows: `.venv\\Scripts\\activate`
5. `pip install -r requirements.txt`
6. `python app.py`
7. Open `http://127.0.0.1:5000`

## Demo
Click **Approval attack**: setApprovalForAll + “I only want to receive an NFT” should produce BLOCK.
Click **Safe transfer**: normal transfer should produce ALLOW.
Click **High-value**: a 150,000 USDC transfer should produce BLOCK (10,000+ alone gives WARN).
Click **Unlimited approval**: approve + Unlimited + "claim my NFT reward" should produce BLOCK with an intent mismatch.
Click **Ownership takeover**: transferOwnership + "receive reward" should produce BLOCK.

Run tests with `pip install pytest` then `python -m pytest`.

## Innovation
The key differentiator is the **Intent–Transaction Consistency Layer**: a technically valid blockchain transaction can still be unsafe if it contradicts the user's stated intent. The prototype turns that mismatch into an explainable security decision.

## Honest claim
This is a hackathon prototype, not a guarantee of perfect detection. For the review, present it as a pre-sign policy firewall that can later connect to live EVM RPC, transaction simulation, contract reputation and wallet/browser extension APIs.
