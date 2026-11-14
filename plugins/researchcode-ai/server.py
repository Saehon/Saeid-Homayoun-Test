#!/usr/bin/env python3
"""ResearchCode AI v0.1.0: dependency-free, read-only MCP server.

Never executes downloaded code, downloads private datasets, or fetches arbitrary URLs.
"""
from __future__ import annotations
import csv
import json
import os
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote, urlparse
from urllib.request import Request, urlopen

VERSION = '0.1.0'
ROOT = Path(__file__).resolve().parent
ALLOWED_HOSTS = {'api.openalex.org', 'api.crossref.org', 'zenodo.org', 'dataverse.harvard.edu'}
DOI_RE = re.compile(r'^10\.\d{4,9}/\S+$', re.I)

class ResearchError(Exception):
    pass

def clean_doi(doi: str) -> str:
    value = doi.strip().removeprefix('https://doi.org/').removeprefix('http://doi.org/').removeprefix('doi:')
    if not DOI_RE.fullmatch(value) or len(value) > 250:
        raise ResearchError('Invalid DOI syntax; expected 10.xxxx/suffix')
    return value

def fetch_json(url: str) -> dict:
    """Limit outbound calls to known public research endpoints; do not follow redirects to arbitrary hosts."""
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname not in ALLOWED_HOSTS:
        raise ResearchError('Request refused: endpoint is not allowlisted HTTPS')
    headers = {'User-Agent': 'ResearchCodeAI/0.1.0 (academic research; public metadata only)', 'Accept': 'application/json'}
    if parsed.hostname == 'api.openalex.org' and os.getenv('OPENALEX_API_KEY'):
        headers['Authorization'] = 'Bearer ' + os.environ['OPENALEX_API_KEY']
    # Redirects are intentionally disabled to avoid credential or SSRF leakage.
    from urllib.request import build_opener, HTTPRedirectHandler
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, hdrs, newurl):
            raise ResearchError('Redirect refused (destination must be reviewed)')
    try:
        with build_opener(NoRedirect).open(Request(url, headers=headers), timeout=12) as resp:
            content = resp.read(1_500_001)
            if len(content) > 1_500_000:
                raise ResearchError('Response exceeds safe size cap')
            return json.loads(content)
    except HTTPError as e:
        if e.code == 429:
            raise ResearchError('Public API rate limit exceeded; retry later or configure your own API key')
        raise ResearchError(f'Public API HTTP {e.code}')
    except (URLError, TimeoutError, json.JSONDecodeError) as e:
        raise ResearchError(f'Public API unavailable or invalid JSON: {type(e).__name__}')

def bounded_text(x, field, max_len=180):
    if not isinstance(x, str) or not x.strip() or len(x)>max_len:
        raise ResearchError(f'{field} must be a non-empty string (max {max_len} chars)')
    return x.strip()

def rankings() -> list[dict]:
    f = Path(os.environ.get('RESEARCHCODE_JOURNAL_CSV', str(ROOT / 'data' / 'journal_registry.csv')))
    if not f.is_file():
        return []
    with f.open(encoding='utf-8-sig', newline='') as fp:
        return list(csv.DictReader(fp))

def classify_journal(journal: str) -> dict:
    journal = bounded_text(journal, 'journal').casefold()
    matches = [x for x in rankings() if x.get('journal','').strip().casefold() == journal]
    verified = [x for x in matches if x.get('verification_status','').lower() == 'verified' and x.get('ranking_edition','').strip() and x.get('source_url','').startswith('https://')]
    if not verified:
        return {'journal': journal, 'status':'unverified','ft50':None,'ajg':None,
            'warning':'Journal tiers are NOT inferred; import a licensed or appropriately sourced official ranking CSV with edition, status and provenance.'}
    r = verified[-1]
    return {'journal':r['journal'], 'status':'verified', 'ft50':r.get('ft50') or None, 'ajg':r.get('ajg') or None,
            'edition':r['ranking_edition'],'source_url':r['source_url']}

def search_publications(query: str, per_page: int = 10, tier: str = '') -> dict:
    query = bounded_text(query,'query',250)
    if type(per_page) is not int or not 1 <= per_page <= 25:
        raise ResearchError('per_page must be an integer from 1 to 25')
    if tier and tier not in ('FT50','4*','4','3'):
        raise ResearchError('tier must be FT50, 4*, 4, 3, or empty')
    if tier and not any(x.get('verification_status')=='verified' for x in rankings()):
        raise ResearchError('Cannot filter by tier without a verified, versioned journal registry')
    url='https://api.openalex.org/works?'+urlencode({'search':query,'per_page':per_page})
    payload = fetch_json(url)
    out=[]
    for x in payload.get('results',[]):
        source=(x.get('primary_location') or {}).get('source') or {}
        journal=source.get('display_name') or ''
        tier_match=classify_journal(journal) if journal else {'status':'unverified'}
        if tier:
            if tier_match.get('status') != 'verified':continue
            if tier == 'FT50' and str(tier_match.get('ft50','')).lower() not in ('true','yes','1'):continue
            if tier in ('3','4','4*') and str(tier_match.get('ajg')) != tier:continue
        doi=(x.get('doi') or '').replace('https://doi.org/','')
        out.append({'title':x.get('title'),'year':x.get('publication_year'),'doi':doi or None,
                    'journal':journal,'ranking':tier_match,
                    'open_access_article':(x.get('open_access') or {}).get('is_oa'),
                    'open_code': 'not_assessed','open_data':'not_assessed',
                    'source_url':x.get('id'),'metadata_provider':'OpenAlex'})
    return {'query':query,'results':out,'returned':len(out),'limitations':'Metadata search, not a complete census; public code/data must be independently verified. Journal list only as supplied and verified.'}

def resolve_doi(doi: str) -> dict:
    doi=clean_doi(doi)
    p=fetch_json('https://api.crossref.org/works/'+quote(doi,safe='/'))['message']
    return {'doi':doi,'title':(p.get('title') or [None])[0],'journal':(p.get('container-title') or [None])[0],
            'publisher':p.get('publisher'),'authors':[(a.get('given','')+' '+a.get('family','')).strip() for a in p.get('author',[])][:20],
            'link':'https://doi.org/'+doi,'metadata_provider':'Crossref', 'provenance':'publisher metadata, not replication verification'}

def find_replication(doi: str) -> dict:
    doi=clean_doi(doi)
    # These are search candidates only; independent article/package linking is required.
    search_term='"'+doi+'"'
    zen=fetch_json('https://zenodo.org/api/records?'+urlencode({'q':search_term,'size':10}))
    har=fetch_json('https://dataverse.harvard.edu/api/search?'+urlencode({'q':doi,'type':'dataset','per_page':10}))
    candidates=[]
    for x in (zen.get('hits') or {}).get('hits',[]):
        meta=x.get('metadata') or {}
        candidates.append({'provider':'Zenodo','title':meta.get('title'), 'url': (x.get('links') or {}).get('self_html') or ('https://zenodo.org/records/'+str(x.get('id'))),
            'license': ((meta.get('license') or {}).get('id') if isinstance(meta.get('license'),dict) else meta.get('license')),
            'match_status':'candidate_unverified'})
    for x in ((har.get('data') or {}).get('items') or []):
        candidates.append({'provider':'Harvard Dataverse','title':x.get('name'),'url':x.get('url'),
            'license':'inspect dataset terms','match_status':'candidate_unverified'})
    return {'article_doi':doi,'candidates':candidates, 'caution':'A search result is not evidence of replication. Verify DOI relations, authors, file lists, licensing, execution, and results before classifying as reproduced.'}

def replication_checklist(doi: str, code_url: str = '', data_url: str = '') -> dict:
    doi=clean_doi(doi)
    urls=[('code_url',code_url),('data_url',data_url)]
    for k,v in urls:
        if v and (urlparse(v).scheme!='https' or not urlparse(v).hostname):
            raise ResearchError(k+' must be a valid https URL')
    steps=['Verify paper DOI, journal, year, and exact version','Verify package association with authors or DOI metadata',
           'Capture license, download conditions, SHA256 checksums, and files','Verify complete data dictionary and sample construction',
           'Pin programming language, packages, operating environment and random seed',
           'Perform malware/license review before any code execution in isolated sandbox',
           'Reproduce tables, coefficients, standard errors, figures and compare tolerances',
           'Report missing/partial reproduction separately from substantive validity']
    return {'doi':doi,'code_url':code_url or None,'data_url':data_url or None,'status':'not_executed',
            'checks':steps,'execution_policy':'No downloaded code is executed by this plugin.'}

def monetary_amount(value, name):
    try:
        if isinstance(value,bool): raise ValueError()
        d=Decimal(str(value))
        if not d.is_finite(): raise ValueError()
        return d
    except (InvalidOperation,ValueError):
        raise ResearchError(name+' must be a finite numeric amount')

def reconciliation(gl_balance, subledger_balance, reconciling_items=None) -> dict:
    items = reconciling_items if reconciling_items is not None else []
    if not isinstance(items,list) or len(items)>1000: raise ResearchError('reconciling_items must be list of <=1000 amounts')
    gl=monetary_amount(gl_balance,'gl_balance'); sub=monetary_amount(subledger_balance,'subledger_balance')
    adj=sum((monetary_amount(v, 'reconciling item') for v in items), Decimal(0))
    unresolved=(gl-sub-adj)
    return {'gl_balance':str(gl),'subledger_balance':str(sub),'items_total':str(adj),
            'unresolved_difference':str(unresolved),'mathematically_balanced':unresolved == 0,
            'caution':'Reconciliation arithmetic is not independent verification of balances, cut-off or supporting evidence.'}

def variance_analysis(actual, comparator):
    a=monetary_amount(actual,'actual'); b=monetary_amount(comparator,'comparator')
    return {'actual':str(a),'comparator':str(b),'difference':str(a-b),
            'percent_change':str(((a-b)/abs(b)*100).quantize(Decimal('0.01'))) if b else None,
            'caution':'No price/volume or causal driver claims without additional inputs.'}

TOOLS = [
 ('search_publications','Search public scholarly metadata; optional FT50/AJG filtering only with verified rankings',{'query':{'type':'string'},'per_page':{'type':'integer'},'tier':{'type':'string'}} ,['query']),
 ('resolve_doi','Retrieve publisher DOI metadata from Crossref',{'doi':{'type':'string'}},['doi']),
 ('find_replication','Find candidate Zenodo/Harvard Dataverse replication deposits by DOI',{'doi':{'type':'string'}},['doi']),
 ('classify_journal','Verify a journal ranking against supplied versioned registry',{'journal':{'type':'string'}},['journal']),
 ('replication_checklist','Return a reproducibility protocol; does not execute code',{'doi':{'type':'string'},'code_url':{'type':'string'},'data_url':{'type':'string'}},['doi']),
 ('reconcile_balances','Check user-supplied GL and subledger amounts',{'gl_balance':{'type':'number'},'subledger_balance':{'type':'number'},'reconciling_items':{'type':'array','items':{'type':'number'}}},['gl_balance','subledger_balance']),
 ('variance_analysis','Calculate numeric variance without inventing drivers',{'actual':{'type':'number'},'comparator':{'type':'number'}},['actual','comparator'])]
TOOL_MAP={x[0]: x for x in TOOLS}
FUNCTIONS={'search_publications':search_publications,'resolve_doi':resolve_doi,'find_replication':find_replication,
           'classify_journal':classify_journal,'replication_checklist':replication_checklist,
           'reconcile_balances':reconciliation,'variance_analysis':variance_analysis}

def handle(request):
    method=request.get('method',''); rid=request.get('id')
    if method == 'initialize':
        return {'jsonrpc':'2.0','id':rid,'result':{'protocolVersion':'2025-06-18','capabilities':{'tools':{}},'serverInfo':{'name':'researchcode-ai','version':VERSION}}}
    if method == 'ping': return {'jsonrpc':'2.0','id':rid,'result':{}}
    if method == 'tools/list':
        return {'jsonrpc':'2.0','id':rid,'result':{'tools':[{'name':name,'description':desc,'inputSchema':{'type':'object','properties':props,'required':required,'additionalProperties':False}} for name,desc,props,required in TOOLS]}}
    if method == 'tools/call':
        params=request.get('params') or {}; name=params.get('name'); args=params.get('arguments') or {}
        if name not in FUNCTIONS: return {'jsonrpc':'2.0','id':rid,'error':{'code':-32602,'message':'Unknown tool'}}
        if not isinstance(args,dict) or any(k not in TOOL_MAP[name][2] for k in args):
            return {'jsonrpc':'2.0','id':rid,'error':{'code':-32602,'message':'Invalid arguments'}}
        try:
            value=FUNCTIONS[name](**args)
            return {'jsonrpc':'2.0','id':rid,'result':{'content':[{'type':'text','text':json.dumps(value,ensure_ascii=False)}],'isError':False}}
        except (ResearchError,TypeError,KeyError) as e:
            return {'jsonrpc':'2.0','id':rid,'result':{'content':[{'type':'text','text':str(e)}],'isError':True}}
    if method.startswith('notifications/') or (rid is None): return None
    return {'jsonrpc':'2.0','id':rid,'error':{'code':-32601,'message':'Method not found'}}

def main():
    for line in sys.stdin:
        try:
            obj=json.loads(line)
            answer=handle(obj)
            if answer is not None:
                print(json.dumps(answer,ensure_ascii=False,separators=(',',':')),flush=True)
        except Exception as e:
            print(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32603,'message':type(e).__name__}}),flush=True)

if __name__=='__main__': main()
