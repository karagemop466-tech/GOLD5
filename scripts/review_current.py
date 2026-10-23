#!/usr/bin/env python3
"""Deterministic evidence-boundary audit. Offline checks do NOT verify seller claims."""
import argparse
import copy
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'review'
DATE = '2026-10-23'
INPUTS = {
    'data/unified.json': 'listings',
    'data/b1f2fe3b_verified_catalog.json': 'entries',
    'site/assets/data.json': 'entries',
    'verification/data.json': 'listings',
    'verified/data/entries.json': 'entries',
    'data/rings.json': None,
    'docs/data/rings.json': None,
    'dossier/data/rings.json': 'rows',
    'dossier/data/rings.jsonl': None,
}
FIELDS = ['priceUsd', 'karat', 'netGoldAlloyGrams', 'solidGold', 'hallmark',
          'makerMark', 'returnPolicy', 'creditCardAccepted', 'spotUsdPerGram',
          'fineGoldGrams', 'metalValueUsd']
E = lambda x: html.escape(str(x), quote=True)

def safe_url(url):
    p = urlsplit(url)
    return p.scheme == 'https' and bool(p.hostname) and not p.username and not p.password

def collect():
    groups = {}
    counts = {}
    for path, key in INPUTS.items():
        raw = (ROOT / path).read_text()
        data = [json.loads(line) for line in raw.splitlines() if line.strip()] if path.endswith('.jsonl') else json.loads(raw)
        rows = data[key] if key else data
        counts[path] = len(rows)
        for n, row in enumerate(rows, 1):
            url = row.get('url')
            assert url and safe_url(url), (path, n, url)
            # Exact URLs only. Different variants/paths are never assumed identical.
            record = groups.setdefault(url, {
                'id': hashlib.sha256(url.encode()).hexdigest()[:16],
                'sourceUrl': url, 'sourceHost': urlsplit(url).hostname,
                'recordedLabels': [], 'recordedCategories': [], 'origins': [],
                'reviewDate': DATE, 'officialPageCheckedAt': None,
                'status': 'unverified', 'flags': ['R01', 'R02', 'R03', 'R04'],
                'current': dict.fromkeys(FIELDS),
            })
            label = row.get('name') or row.get('title') or row.get('product') or str(row.get('id'))
            if label not in record['recordedLabels']: record['recordedLabels'].append(label)
            cat = row.get('category')
            if cat and cat not in record['recordedCategories']: record['recordedCategories'].append(cat)
            record['origins'].append({'file': path, 'row': n, 'recordedId': row.get('id')})
    return {'reviewDate': DATE, 'scope': 'All product records in the nine enumerated repository datasets; not a complete market inventory.',
            'method': 'Exact source URL grouping, no inferred product equivalence. Historical labels are navigation aids, not confirmed specifications.',
            'sourceAccess': 'Restricted egress; no merchant or gold-price source reverified in this session. Blue Nile curl probe failed with SSL_ERROR_SYSCALL.',
            'inputCounts': counts, 'entries': sorted(groups.values(), key=lambda r: r['sourceUrl'])}

def validate(data):
    assert data['reviewDate'] == DATE
    assert data['entries']
    assert len({r['id'] for r in data['entries']}) == len(data['entries'])
    for r in data['entries']:
        assert safe_url(r['sourceUrl'])
        assert r['status'] == 'unverified'
        assert r['officialPageCheckedAt'] is None
        assert r['flags'] and r['origins']
        assert set(r['current']) == set(FIELDS)
        assert all(v is None for v in r['current'].values()), 'Unsupported current claim'
        for origin in r['origins']:
            assert origin['file'] in INPUTS and origin['row'] > 0
    assert sum(data['inputCounts'].values()) == sum(len(r['origins']) for r in data['entries'])

STYLE = '''body{margin:0;background:#f6f4ef;color:#202c2a;font:16px/1.6 system-ui,sans-serif}main,header{max-width:1250px;margin:auto;padding:24px}header{border-bottom:1px solid #c5c6bd}nav{display:flex;gap:20px;flex-wrap:wrap}a{color:#275e50}h1{font:normal 42px/1.2 Georgia,serif}h2{font:normal 28px Georgia,serif}.notice{background:#fff2cf;border-left:5px solid #9b782c;padding:18px}.card{background:white;padding:22px;border:1px solid #deded4;border-radius:10px;margin:20px 0}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;vertical-align:top;border-bottom:1px solid #ddd;padding:12px}th{background:#e9ede7}small{display:block;color:#52605a}code{overflow-wrap:anywhere}summary{cursor:pointer}a:focus-visible{outline:3px solid #9b782c}'''

def page(title, content):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} · GOLD5</title><link rel="stylesheet" href="review.css"></head><body><header><strong>GOLD5 / EVIDENCE REVIEW</strong><nav><a href="../index.html">Dashboard</a><a href="index.html">Current evidence</a><a href="categories.html">Categories</a><a href="flagged.html">Flagged for Review</a><a href="calculation.html">Gold calculations</a><a href="../site/checklist.html">Buying checklist (historical)</a></nav></header><main><div class="notice"><b>NO HALLUCINATIONS.</b> Reviewed {DATE}. No current merchant prices or specifications independently confirmed. Blank cells mean unverified, not zero. Historical claims are not proof of purity. Recheck for hallucinations after every review.</div><h1>{E(title)}</h1>{content}<p>Automated tests check provenance structure, blank-field policy and links—not truth, source freshness, seller reputation or physical gold purity.</p></main></body></html>'''

def table(rows):
    body = ''
    for r in rows:
        origins = ''.join(f'<li><a href="../{E(o["file"])}">{E(o["file"])} · record {o["row"]}</a> ({E(o["recordedId"])})</li>' for o in r['origins'])
        body += f'''<tr id="{r['id']}"><td>{E(r['recordedLabels'][0])}<small>Historical label only</small><details><summary>Original records ({len(r['origins'])})</summary><ul>{origins}</ul></details></td><td><a href="{E(r['sourceUrl'])}">{E(r['sourceHost'])} ↗</a></td><td></td><td></td><td></td><td><a href="flagged.html">Unverified · R01–R04</a><small>Review: {DATE}<br>Official recheck: not performed</small></td></tr>'''
    return '<div class="scroll"><table><thead><tr><th>Recorded candidate</th><th>Recorded official / seller source</th><th>Current USD</th><th>Confirmed karat</th><th>Net alloy g</th><th>Evidence state</th></tr></thead><tbody>' + body + '</tbody></table></div>'

def outputs(data):
    rows = data['entries']
    count = sum(data['inputCounts'].values())
    inventory = ''.join(f'<tr><td><a href="../{p}">{p}</a></td><td>{n}</td></tr>' for p,n in data['inputCounts'].items())
    intro = f'''<p>{count} stored records grouped into <b>{len(rows)} exact source URLs</b>. This is a repository inventory, not {len(rows)} distinct rings or an exhaustive market list. Marketplace and category URLs remain candidates; inclusion is not an endorsement.</p><p><b>Purchase-ready recommendations: none established by this review.</b> No manual input is required to browse. Official re-verification remains blocked by this session's network restrictions.</p><p><a href="current.json">Download machine-readable ledger</a> · <a href="checks.json">Automated check results</a></p>'''
    categories = sorted({c for r in rows for c in r['recordedCategories']})
    cats = '<p>Categories below are inherited labels, not newly verified product attributes. A URL may appear in more than one category. Uncategorized candidates remain in the full inventory.</p>'
    for c in categories:
        subset = [r for r in rows if c in r['recordedCategories']]
        cats += f'<details class="card"><summary>{E(c)} ({len(subset)} source URLs)</summary>{table(subset)}</details>'
    cats += '<h2>Uncategorized</h2>' + table([r for r in rows if not r['recordedCategories']])
    flags = '''<p>All candidates require review; these flags do not block publishing the research.</p><div class="card"><h2>R01 — Current evidence unavailable</h2><p>No merchant pages were re-fetched successfully. Prior captures are retained separately but not asserted as current. A URL is a review lead, not evidence that its contents are accessible or correct.</p><h2>R02 — Historical verification wording</h2><p>Earlier pages call listings and spot prices “verified.” Treat these as previous sessions' dated claims, not independently confirmed findings of this review. Passing scripts cannot detect every fabricated or inaccurate source excerpt.</p><h2>R03 — Physical purity and purchase eligibility unresolved</h2><p>No independent assay, maker-mark inspection, net metal weight, current return exclusions or payment protections were established here. A seller's karat claim alone does not authenticate a ring. Do not classify these candidates as meeting the full buying checklist.</p><h2>R04 — Duplicate and variant ambiguity</h2><p>Exact URL matches are grouped only. Different URLs can describe the same product; the same URL may offer different metals, sizes, currencies or stones. Historical titles and categories must not populate confirmed specification fields.</p></div><h2>Affected candidates and official-source review links</h2>'''
    calc = '''<div class="card"><h2>Current valuation: unavailable</h2><p>Confirmed net gold-alloy weight, fineness and current spot price are blank for every candidate. Therefore current fine-gold amounts and metal values are also blank. No old quote is silently used as a current price.</p><p>Calculation method: fine-gold grams = net gold-alloy grams × confirmed fineness; metal value = fine-gold grams × dated spot price per gram. These are derived estimates, not purchase prices, resale offers or authentication tests. Gross ring weight including stones must not be treated as net alloy weight.</p><p><a href="../site/calculator.html">Open the existing historical/scenario calculator</a>. Its prefilled numbers are historical claims, not reverified current inputs. It requires inputs for hypothetical scenarios; no user input is needed for this research inventory.</p></div>'''
    return {
        'current.json': json.dumps(data, indent=2, ensure_ascii=False)+'\n',
        'index.html': page('Current evidence inventory', intro + table(rows) + '<h2>Dataset coverage</h2><table><tr><th>Repository source</th><th>Records</th></tr>'+inventory+'</table>'),
        'categories.html': page('Browse recorded categories', cats),
        'flagged.html': page('Flagged for Review', flags+table(rows)),
        'calculation.html': page('Gold weight and raw-gold calculations', calc),
        'review.css': STYLE,
    }

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    data = collect(); validate(data)
    caught = 0
    for mutate in [lambda r:r['current'].update(priceUsd=1),lambda r:r.update(status='verified'),lambda r:r.update(sourceUrl='javascript:alert(1)'),lambda r:r.update(officialPageCheckedAt=DATE),lambda r:r.update(flags=[]),lambda r:r['current'].update(fineGoldGrams=2)]:
        bad=copy.deepcopy(data); mutate(bad['entries'][0])
        try: validate(bad)
        except AssertionError: caught += 1
    assert caught == 6
    files=outputs(data)
    from html.parser import HTMLParser
    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, val in attrs:
                if key.lower().startswith('on'): raise AssertionError('Inline event handler')
                if key not in ('href','src') or not val: continue
                if urlsplit(val).scheme:
                    assert safe_url(val), val
                else:
                    path=val.split('#')[0]
                    assert (OUT/path).exists() or path in files or path == 'checks.json', val
            assert tag not in ('script','iframe','form'), tag
    for name, content in files.items():
        if name.endswith('.html'): Links().feed(content)
    report={'reviewDate':DATE,'result':'PASS','inputRecords':sum(data['inputCounts'].values()),'exactSourceUrls':len(data['entries']),'negativeTestsCaught':caught,'negativeTestsTotal':6,'checks':['all stored rows accounted for','source URLs HTTPS; rendered text escaped','all current facts and derived values blank','no unsupported verified state or source-check date','all rows flagged and linked to origins','generated local links resolve','no scripts, frames, forms or inline event handlers','deterministic output comparison in check mode'],'limitations':'Offline structural checks only. No source truth, external link availability, physical purity or current price verified.'}
    files['checks.json']=json.dumps(report,indent=2)+'\n'
    for name, content in files.items():
        if args.check: assert (OUT/name).read_text()==content, f'Stale output: {name}'
        else: (OUT/name).write_text(content)
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
