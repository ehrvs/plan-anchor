#!/usr/bin/env python3
from __future__ import annotations
import argparse, concurrent.futures, datetime, hashlib, importlib.util, json, os, pathlib, statistics, time

ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base_a0',ROOT/'run_calibration.py'); base=importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
ROUND=ROOT/'round3-affected-only'

def q(i,y,n,u): return base.choice_question(i,y,n,u)

def pool(): return {
 'faithful':{
  'faithful-r3-a-source-coverage':q(
   'Does anchor.quote directly support the substantive obligation in anchor.statement? Formal requirement wording and selecting one directive from a multi-directive quote are allowed. Added technical specificity such as an algorithm, strength, mechanism, policy, or outcome absent from the quote is not supported.',
   'The statement formalizes a quoted directive without adding substantive specificity; unrelated quoted directives may be separate anchors.',
   'The statement adds or changes substantive specificity that the quote does not supply.',
   'The quote has multiple plausible meanings, so support cannot be settled.'),
  'faithful-r3-b-supported-specificity':q(
   'Is every substantive detail required by anchor.statement present in or necessarily implied by anchor.quote? Do not require the statement to repeat unrelated directives from the same quote, and treat informal should/need wording as directive provenance.',
   'Every required substantive detail is supported or necessarily implied by the quote.',
   'At least one required mechanism, strength, policy, condition, or outcome is absent from the quote.',
   'Ambiguity in the quote prevents determining support.'),
  'faithful-r3-c-atomic-entailment':q(
   'For this one atomic statement, does anchor.quote entail its required action and outcome? A longer quote may entail several separate anchors. Formalizing an informal directive is faithful; choosing an unmentioned implementation detail is not.',
   'The action and outcome follow from the quote without an extra decision.',
   'The action or outcome requires an extra decision not supplied by the quote.',
   'The quote is too indeterminate to decide entailment.'),
 },
 'self_contained':{
  'self-r3-a-disqualifiers':q(
   'Is anchor.statement independently understandable and applicable without any of these disqualifiers: an undefined subjective quality (for example robust), private shorthand, or a human approval that has no identified recorded artifact? Ignore grammar, bundling, fidelity, and scope.',
   'None of those outside-context dependencies is needed; ordinary technical terms, concrete prohibitions, lists, and explicit input/action/outcome conditions are sufficient.',
   'At least one decisive term is an undefined quality or private label, or compliance depends on an approval with no identified record.',
   'A possible outside-context dependency exists but the statement does not show whether it is decisive.'),
  'self-r3-b-outside-information':q(
   'Can a reviewer determine what behavior anchor.statement requires using the statement itself, without asking what a vague quality or private code means and without discovering whether an unrecorded person approved it? Judge meaning only; other questions judge grammar, atomicity, source support, and scope.',
   'Yes; the behavior and conditions have enough ordinary or explicit meaning for independent application.',
   'No; a vague/private meaning or an unrecorded approval is necessary to apply it.',
   'Most meaning is available, but a material dependency remains ambiguous.'),
  'self-r3-c-complete-decision-rule':q(
   'Does anchor.statement itself provide a complete decision rule for its described behavior? Explicit negative rules and explicit conditions pass. A word such as robust, an undefined code such as R7, or approval with no specified record does not provide a complete decision rule. Ignore sentence form and quote fidelity.',
   'The described behavior has a complete rule that an independent reviewer can apply.',
   'The rule is incomplete because a decisive quality, code, or approval is undefined or unrecorded.',
   'The rule contains some decision information but remains materially ambiguous.'),
 }}

def freeze():
 ROUND.mkdir(parents=True,exist_ok=True); data={'schema':'plan-anchor/testability-candidate-pool/1','round':3,'evaluation_mode':'affected-role-isolated','corpus_sha256':base.digest_file(ROOT/'corpus.frozen.json'),'semantic_candidates':pool(),'candidate_count':6,'prior_round_preserved':str(ROOT/'round2-role-isolated/semantic-evaluations.json')}
 base.write_json(ROUND/'candidates-round3.frozen.json',data,True); fm={'schema':'plan-anchor/testability-round-freeze/1','round':3,'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'first_live_call_at':None,'corpus_sha256':data['corpus_sha256'],'candidate_pool_sha256':base.digest_file(ROUND/'candidates-round3.frozen.json')}; base.write_json(ROUND/'freeze-manifest.json',fm,True); print(json.dumps(fm,indent=2,sort_keys=True))

def live():
 fm=base.load_json(ROUND/'freeze-manifest.json');
 if fm['first_live_call_at'] is not None: raise SystemExit('round already started')
 corpus=base.load_json(ROOT/'corpus.frozen.json'); candidates=base.load_json(ROUND/'candidates-round3.frozen.json')['semantic_candidates']; key=os.environ.get('TYPESAFE_API_KEY','').strip()
 if not key: raise SystemExit('TYPESAFE_API_KEY missing')
 if any(k.startswith('PLAN_ANCHOR_') for k in os.environ): raise SystemExit('PLAN_ANCHOR_* environment variables forbidden')
 jj=base.jev_module(); first=datetime.datetime.now(datetime.timezone.utc).isoformat(); fm['first_live_call_at']=first; base.write_json(ROUND/'freeze-manifest.json',fm,True)
 jobs=[]
 for repeat in (1,2):
  for role,questions in candidates.items():
   for item in corpus['semantic_cases']: jobs.append((role,item['case_id'],repeat,{'model':'jev-latest','questions':questions,'state':item['state']}))
 def one(job):
  role,cid,repeat,body=job; started=time.monotonic(); response,meta=jj.judge_with_policy(body,key,30.0,24000,2000,body['questions'],shorten=False); rid=f"a0-r3-{role}-{cid}-r{repeat}-{hashlib.sha256((first+role+cid+str(repeat)).encode()).hexdigest()[:12]}"; record={'schema':'plan-anchor/direct-jev-evidence/1','run_id':rid,'role':role,'case_id':cid,'repeat':repeat,'request_sha256':base.digest_obj(body),'canonical_request':body,'raw_response':response,'transport_meta':meta,'duration_ms':round((time.monotonic()-started)*1000),'model_requested':'jev-latest','policy':{'timeout_seconds':30.0,'max_request_bytes':24000,'shorten':False,'allow_remote':True,'environment_allowlist':['TYPESAFE_API_KEY']}}; path=ROUND/'runs'/role/f'{cid}-r{repeat}.json'; base.write_json(path,record,True); return {'role':role,'case_id':cid,'repeat':repeat,'run_id':rid,'path':str(path),'request_sha256':record['request_sha256']}
 results=[]
 for repeat in (1,2):
  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex: results.extend(ex.map(one,[j for j in jobs if j[2]==repeat]))
  if repeat==1: time.sleep(1.1)
 base.write_json(ROUND/'execution-manifest.json',{'schema':'plan-anchor/a0-execution/1','runs':results},True); analyze(corpus,candidates,results)

def analyze(corpus,candidates,results):
 runs={(r['role'],r['case_id'],r['repeat']):base.load_json(r['path']) for r in results}; evals=[]; identities=[]
 for role,questions in candidates.items():
  for item in corpus['semantic_cases']:
   a,b=runs[(role,item['case_id'],1)],runs[(role,item['case_id'],2)]; identities.append({'role':role,'case_id':item['case_id'],'request_sha256':a['request_sha256'],'byte_identical':base.canonical(a['canonical_request'])==base.canonical(b['canonical_request'])})
  for cid,question in questions.items():
   cells=[]
   for item in corpus['semantic_cases']:
    answers=[runs[(role,item['case_id'],r)]['raw_response']['answers'][cid] for r in (1,2)]; tuples=[base.answer_tuple(a) for a in answers]; expected=item['expected'][role]; ok=all(c==expected and p>=base.PRODUCTION_THRESHOLD for c,p in tuples); cells.append({'case_id':item['case_id'],'expected':expected,'answers':answers,'accepted':ok,'stable':tuples[0][0]==tuples[1][0],'confident':all(p>=base.PRODUCTION_THRESHOLD for _,p in tuples)})
   conf=[base.answer_tuple(a)[1] for cell in cells for a in cell['answers']]; evals.append({'role':role,'candidate_id':cid,'question':question,'accepted':all(c['accepted'] for c in cells),'exact_cells':sum(c['accepted'] for c in cells),'total_cells':len(cells),'stable_cells':sum(c['stable'] for c in cells),'confident_cells':sum(c['confident'] for c in cells),'minimum_confidence':min(conf),'mean_confidence':statistics.mean(conf),'cells_at_or_above_diagnostic':sum(p>=base.DIAGNOSTIC_THRESHOLD for p in conf),'total_answers':len(conf),'cells':cells})
 base.write_json(ROUND/'repeat-request-identity.json',{'schema':'plan-anchor/repeat-request-identity/1','pairs':identities},True); base.write_json(ROUND/'semantic-evaluations.json',evals,True)
 def rk(e): return (-int(e['accepted']),-e['exact_cells'],-e['stable_cells'],-e['confident_cells'],-e['cells_at_or_above_diagnostic'],-e['minimum_confidence'],-e['mean_confidence'],len(base.canonical(e['question'])),e['candidate_id'])
 rankings={}; selected={}
 for role in candidates:
  ranked=sorted([e for e in evals if e['role']==role],key=rk); rankings[role]=[e['candidate_id'] for e in ranked]
  if ranked[0]['accepted']: selected[role]=ranked[0]
 summary={'schema':'plan-anchor/a0-round-summary/1','round':3,'accepted':len(selected)==2,'selected_candidates':{k:v['candidate_id'] for k,v in selected.items()},'rankings':rankings,'corpus_sha256':base.digest_file(ROOT/'corpus.frozen.json'),'candidate_pool_sha256':base.digest_file(ROUND/'candidates-round3.frozen.json'),'all_repeat_requests_byte_identical':all(x['byte_identical'] for x in identities),'unique_run_ids':len({r['run_id'] for r in results})==len(results),'live_run_count':len(results),'production_confidence_threshold':base.PRODUCTION_THRESHOLD,'confidence_reference_threshold':base.DIAGNOSTIC_THRESHOLD}; base.write_json(ROUND/'round-summary.json',summary,True); print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('mode',choices=('freeze','live')); a=p.parse_args(); freeze() if a.mode=='freeze' else live()
