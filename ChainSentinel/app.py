from flask import Flask, render_template, request, jsonify
import sqlite3, json, hashlib
from datetime import datetime, timezone
app=Flask(__name__); DB='data/chainsentinel.db'
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 c=db(); c.execute('CREATE TABLE IF NOT EXISTS scans(id INTEGER PRIMARY KEY AUTOINCREMENT,wallet TEXT,chain TEXT,action TEXT,target TEXT,amount REAL,token TEXT,risk_score INTEGER,verdict TEXT,reasons TEXT,created_at TEXT)'); c.execute('CREATE TABLE IF NOT EXISTS watchlist(id INTEGER PRIMARY KEY AUTOINCREMENT,address TEXT UNIQUE,label TEXT,chain TEXT,created_at TEXT)'); c.commit(); c.close()
KNOWN={'0x000000000000000000000000000000000000dead','0x1111111111111111111111111111111111111111'}
SUSP={'setApprovalForAll','approve','permit','transferFrom','upgradeTo','transferOwnership','renounceOwnership','grantRole','setOwner'}; DANG={'setApprovalForAll','upgradeTo','transferOwnership','renounceOwnership','grantRole','setOwner'}
BENIGN=('receive','claim','mint','view','connect','login','reward','airdrop')
UNLIMITED=1e30
def parse_amount(v):
 if isinstance(v,str) and v.strip().lower() in {'unlimited','max','infinite'}:return UNLIMITED
 try:
  x=float(v or 0)
 except (TypeError,ValueError):
  return 0.0
 return min(x,UNLIMITED) if x==x else 0.0
def score_tx(t):
 s=0; r=[]; a=t.get('action',''); target=t.get('target','').lower(); amount=parse_amount(t.get('amount')); chain=t.get('chain','Ethereum'); intent=t.get('intent','').lower()
 if target in KNOWN:s+=65;r.append('Target address is on the local malicious-address watchlist.')
 if a in DANG:s+=35;r.append(f'Privileged contract action detected: {a}.')
 elif a in SUSP:s+=22;r.append(f'Token/contract permission action detected: {a}.')
 if amount>=UNLIMITED:s+=30;r.append('Unlimited amount requested: the spender could drain every token of this type.')
 elif amount>=10000:s+=40;r.append('High-value transaction exceeds the demo safety threshold.')
 if UNLIMITED>amount>=100000:s+=30;r.append('Very high-value transaction requires enhanced verification.')
 if chain.lower() not in {'ethereum','polygon','base','arbitrum','sepolia'}:s+=18;r.append('Unrecognized chain in the local policy registry.')
 if a in SUSP and any(w in intent for w in BENIGN):s+=35;r.append(f'Intent mismatch: your stated goal ("{t.get("intent","")[:60]}") should not need the permission action {a}.')
 if not target.startswith('0x') or len(target)!=42:s+=10;r.append('Target does not match the expected EVM address format.')
 if not r:r.append('No high-risk pattern matched the configured policy rules.')
 s=min(100,s); v='BLOCK' if s>=70 else ('WARN' if s>=40 else 'ALLOW'); return s,v,r
@app.route('/')
def index():return render_template('index.html')
@app.post('/api/scan')
def scan():
 t=request.get_json(force=True); s,v,r=score_tx(t); c=db(); c.execute('INSERT INTO scans(wallet,chain,action,target,amount,token,risk_score,verdict,reasons,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(t.get('wallet',''),t.get('chain',''),t.get('action',''),t.get('target',''),parse_amount(t.get('amount')),t.get('token',''),s,v,json.dumps(r),datetime.now(timezone.utc).isoformat())); c.commit(); c.close(); sid=hashlib.sha256((json.dumps(t,sort_keys=True)+str(datetime.now())).encode()).hexdigest()[:12]; return jsonify(risk_score=s,verdict=v,reasons=r,scan_id=sid,recommended_action='Do not sign this transaction.' if v=='BLOCK' else ('Verify contract, spender and permissions before signing.' if v=='WARN' else 'Transaction passes the current local policy.'))
@app.get('/api/history')
def history():
 c=db(); rows=c.execute('SELECT * FROM scans ORDER BY id DESC LIMIT 20').fetchall(); c.close(); return jsonify([dict(x) for x in rows])
@app.get('/api/stats')
def stats():
 c=db(); out={k:c.execute('SELECT COUNT(*) c FROM scans WHERE verdict=?',(v,)).fetchone()['c'] for k,v in [('blocked','BLOCK'),('warned','WARN'),('allowed','ALLOW')]}; out['total']=sum(out.values()); c.close(); return jsonify(out)
init_db()
if __name__=='__main__': app.run(debug=False,host='127.0.0.1',port=5000)
