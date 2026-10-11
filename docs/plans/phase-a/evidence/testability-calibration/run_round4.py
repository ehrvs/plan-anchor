#!/usr/bin/env python3
from __future__ import annotations
import argparse, concurrent.futures, datetime, hashlib, importlib.util, json, os, pathlib, statistics, time
ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base_a0',ROOT/'run_calibration.py'); base=importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
ROUND=ROOT/'round4-faithful-only'
def q(i,y,n,u): return base.choice_question(i,y,n,u)
def pool(): return {
 'faithful-r4-a-no-unsupported-addition':q(
  'Narrow fidelity check: does anchor.statement avoid adding any substantive obligation that is absent from anchor.quote? Answer yes for a formal paraphrase even when the shared requirement is vague, the quote says should/need rather than must, common equivalent terms are used, or the statement isolates one directive from a longer quote. Other questions judge quality and completeness.',
  'The statement is a semantic paraphrase or atomic subset of the quote and introduces no new substantive policy, mechanism, strength, condition, or outcome.',
  'The statement introduces or changes at least one substantive policy, mechanism, strength, condition, or outcome not supported by the quote.',
  'The quote has genuinely competing meanings, so unsupported addition cannot be determined.'),
 'faithful-r4-b-formal-paraphrase':q(
  'Is anchor.statement a faithful formal requirement derived from anchor.quote? Preserve meaning, not wording: informal directives may become must, print may become emit to stdout, machine-readable JSON may become JSON, and one directive in a compound quote may become one anchor. Do not penalize vagueness here.',
  'Those normalization rules are sufficient and no substantive requirement was invented.',
  'Even after ordinary normalization, the statement requires a new policy, implementation choice, strength, trigger, or outcome.',
  'Ordinary normalization does not settle whether the meaning was preserved.'),
 'faithful-r4-c-semantic-subset':q(
  'Does the substantive obligation in anchor.statement form a supported semantic subset of anchor.quote? The quote may contain additional independent directives. A repeated vague term is still faithful to itself; testability is judged elsewhere.',
  'Every substantive element of the statement is supported by the quote, although the quote may say more.',
  'At least one substantive element of the statement is absent from or conflicts with the quote.',
  'The quote is too ambiguous to decide whether all statement elements are supported.')}
def freeze():
 ROUND.mkdir(parents=True,exist_ok=True); data={'schema':'plan-anchor/testability-candidate-pool/1','round':4,'evaluation_mode':'faithful-only','corpus_sha256':base.digest_file(ROOT/'corpus.frozen.json'),'semantic_candidates':{'faithful':pool()},'candidate_count':3,'prior_round_preserved':str(ROOT/'round3-affected-only/semantic-evaluations.json')}; base.write_json(ROUND/'candidates-round4.frozen.json',data,True); fm={'schema':'plan-anchor/testability-round-freeze/1','round':4,'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_live_call_at':None,'corpus_sha256':data['corpus_sha256'],'candidate_pool_sha256':base.digest_file(ROUND/'candidates-round4.frozen.json')}; base.write_json(ROUND/'freeze-manifest.json',fm,True); print(json.dumps(fm,indent=2,sort_keys=True))
def live():
 fm=base.load_json(ROUND/'freeze-manifest.json');
 if fm['first_live_call_at'] is not None: raise SystemExit('round already started')
 corpus=base.load_json(ROOT/'corpus.frozen.json'); questions=pool(); key=os.environ.get('TYPESAFE_API_KEY','').strip()
 if not key: raise SystemExit('TYPESAFE_API_KEY missing')
 if any(k.startswith('PLAN_ANCHOR_') for k in os.environ): raise SystemExit('PLAN_ANCHOR_* environment variables forbidden')
 jj=base.jev_module(); first=datetime.datetime.now(datetime.timezone.utc).isoformat(); fm['first_live_call_at']=first; base.write_json(ROUND/'freeze-manifest.json',fm,True)
 jobs=[(item['case_id'],repeat,{'model':'jev-latest','questions':questions,'state':item['state']}) for repeat in (1,2) for item in corpus['semantic_cases']]
 def one(job):
  cid,repeat,body=job; started=time.monotonic(); response,meta=jj.judge_with_policy(body,key,30.0,24000,2000,questions,shorten=False); rid=f"a0-r4-faithful-{cid}-r{repeat}-{hashlib.sha256((first+cid+str(repeat)).encode()).hexdigest()[:12]}"; record={'schema':'plan-anchor/direct-jev-evidence/1','run_id':rid,'role':'faithful','case_id':cid,'repeat':repeat,'request_sha256':base.digest_obj(body),'canonical_request':body,'raw_response':response,'transport_meta':meta,'duration_ms':round((time.monotonic()-started)*1000),'model_requested':'jev-latest','policy':{'timeout_seconds':30.0,'max_request_bytes':24000,'shorten':False,'allow_remote':True,'environment_allowlist':['TYPESAFE_API_KEY']}}; path=ROUND/'runs'/f'{cid}-r{repeat}.json'; base.write_json(path,record,True); return {'case_id':cid,'repeat':repeat,'run_id':rid,'path':str(path),'request_sha256':record['request_sha256']}
 results=[]
 for repeat in (1,2):
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex: results.extend(ex.map(one,[j for j in jobs if j[1]==repeat]))
  if repeat==1: time.sleep(1.1)
 base.write_json(ROUND/'execution-manifest.json',{'schema':'plan-anchor/a0-execution/1','runs':results},True); analyze(corpus,questions,results)
def analyze(corpus,questions,results):
 runs={(r['case_id'],r['repeat']):base.load_json(r['path']) for r in results}; identities=[]; evals=[]
 for item in corpus['semantic_cases']:
  a,b=runs[(item['case_id'],1)],runs[(item['case_id'],2)]; identities.append({'case_id':item['case_id'],'request_sha256':a['request_sha256'],'byte_identical':base.canonical(a['canonical_request'])==base.canonical(b['canonical_request'])})
 for cid,question in questions.items():
  cells=[]
  for item in corpus['semantic_cases']:
   answers=[runs[(item['case_id'],r)]['raw_response']['answers'][cid] for r in (1,2)]; tuples=[base.answer_tuple(a) for a in answers]; expected=item['expected']['faithful']; ok=all(c==expected and p>=base.PRODUCTION_THRESHOLD for c,p in tuples); cells.append({'case_id':item['case_id'],'expected':expected,'answers':answers,'accepted':ok,'stable':tuples[0][0]==tuples[1][0],'confident':all(p>=base.PRODUCTION_THRESHOLD for _,p in tuples)})
  conf=[base.answer_tuple(a)[1] for cell in cells for a in cell['answers']]; evals.append({'role':'faithful','candidate_id':cid,'question':question,'accepted':all(c['accepted'] for c in cells),'exact_cells':sum(c['accepted'] for c in cells),'total_cells':len(cells),'stable_cells':sum(c['stable'] for c in cells),'confident_cells':sum(c['confident'] for c in cells),'minimum_confidence':min(conf),'mean_confidence':statistics.mean(conf),'cells_at_or_above_diagnostic':sum(p>=base.DIAGNOSTIC_THRESHOLD for p in conf),'total_answers':len(conf),'cells':cells})
 base.write_json(ROUND/'repeat-request-identity.json',{'schema':'plan-anchor/repeat-request-identity/1','pairs':identities},True); base.write_json(ROUND/'semantic-evaluations.json',evals,True)
 def rk(e): return (-int(e['accepted']),-e['exact_cells'],-e['stable_cells'],-e['confident_cells'],-e['cells_at_or_above_diagnostic'],-e['minimum_confidence'],-e['mean_confidence'],len(base.canonical(e['question'])),e['candidate_id'])
 ranked=sorted(evals,key=rk); selected=ranked[0] if ranked[0]['accepted'] else None; summary={'schema':'plan-anchor/a0-round-summary/1','round':4,'accepted':selected is not None,'selected_candidate':selected['candidate_id'] if selected else None,'ranking':[e['candidate_id'] for e in ranked],'corpus_sha256':base.digest_file(ROOT/'corpus.frozen.json'),'candidate_pool_sha256':base.digest_file(ROUND/'candidates-round4.frozen.json'),'all_repeat_requests_byte_identical':all(x['byte_identical'] for x in identities),'unique_run_ids':len({r['run_id'] for r in results})==len(results),'live_run_count':len(results),'production_confidence_threshold':base.PRODUCTION_THRESHOLD,'confidence_reference_threshold':base.DIAGNOSTIC_THRESHOLD}; base.write_json(ROUND/'round-summary.json',summary,True); print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=('freeze','live'));a=p.parse_args();freeze() if a.mode=='freeze' else live()
