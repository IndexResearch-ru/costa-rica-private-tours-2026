#!/usr/bin/env python3
"""Reproducible integrity checks for Costa Rica 1.0.0, no ranking."""
import csv,json
from pathlib import Path
from collections import Counter
p=Path(__file__).resolve().parent
with (p/'SOURCE_REGISTER.csv').open(encoding='utf-8-sig',newline='') as f:src=list(csv.DictReader(f))
with (p/'FACT_CLAIM_MAP.csv').open(encoding='utf-8-sig',newline='') as f:cl=list(csv.DictReader(f))
with (p/'OBSERVATION_MATRIX.csv').open(encoding='utf-8-sig',newline='') as f:mx=list(csv.DictReader(f))
res=json.loads((p/'RESULTS.json').read_text('utf8'))
faq=json.loads((p/'FAQ_DATA.json').read_text('utf8'))
assert len(src)==45 and len(cl)==120 and len(mx)==20 and len(faq)==9
ids={s['source_id'] for s in src};assert len(ids)==45
assert len({c['claim_id'] for c in cl})==120
assert len({(c['candidate_id'],c['field_id']) for c in cl})==120
assert {c['field_id'] for c in cl}=={'M1','M2','M3','M4','M5','M6'}
assert {c['candidate_id'] for c in cl}=={x['candidate_id'] for x in mx}
assert sum(c['evidence_status']=='ОПИСАНО_В_ИСТОЧНИКЕ' for c in cl)==84
assert sum(c['evidence_status']=='НЕ_ПОДТВЕРЖДЕНО_В_ПРОСМОТРЕННЫХ_ИСТОЧНИКАХ' for c in cl)==36
for c in cl:
 refs=[x for x in c['source_ids'].split(';') if x]
 assert all(x in ids for x in refs)
 if c['evidence_status']=='ОПИСАНО_В_ИСТОЧНИКЕ':assert refs
assert len(res['companies'])==20
assert all(len(x['observations'])==6 for x in res['companies'])
assert res['noRanking'] and res['scores'] is None and res['weights'] is None and res['ranks'] is None
assert res['publicationDecision']=='PUBLISH'
print('QA PASS: 20 companies, 6 fields, 120 claims, 84 documented / 36 unconfirmed, 45 sources, no ranking.')
