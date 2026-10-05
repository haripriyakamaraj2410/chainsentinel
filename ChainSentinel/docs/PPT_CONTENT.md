# PPT CONTENT

## 1. Title
**ChainSentinel: Intent-Aware Web3 Transaction Security Firewall**
Stop dangerous blockchain actions before the user signs.

## 2. Problem
Users can be tricked into signing approvals and permissions they do not understand. A transaction can be technically valid but still violate the user's actual intent.

## 3. Innovation
An **Intent–Transaction Consistency Layer** compares stated intent with action, target, value, token and chain policy. Output: ALLOW / WARN / BLOCK with reasons.

## 4. Architecture
User Intent → Transaction Parser → Risk/Policy Engine → Intent-Mismatch Detector → Decision Firewall → Explainable Alert + Audit Trail

## 5. Implementation
HTML/CSS/JS + Flask + SQLite + explainable weighted rules.

## 6. Demo
Safe transfer → ALLOW; approval attack + receive intent → BLOCK; high-value transfer → WARN/BLOCK.

## 7. Impact
Reduces accidental signing risk, improves security comprehension, and can be integrated as a wallet/browser pre-sign layer.

## 8. Future
Live RPC, transaction simulation, contract reputation, browser extension, multichain policies and NLP/ML intent extraction.

**Do not claim 100% cybersecurity accuracy.** Say “prototype security decision engine with explainable scoring.”
