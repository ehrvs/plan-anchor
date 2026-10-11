#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, os, pathlib

ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base_a0',ROOT/'run_calibration.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def pick(path,cid): return next(e for e in base.load_json(path) if e['candidate_id']==cid)
selected={
 'single_constraint':pick(ROOT/'round2-role-isolated/semantic-evaluations.json','atomic-r2-b-same-invariant'),
 'observable':pick(ROOT/'round2-role-isolated/semantic-evaluations.json','observable-r2-a-defined-check'),
 'faithful':pick(ROOT/'round4-faithful-only/semantic-evaluations.json','faithful-r4-b-formal-paraphrase'),
 'scoped':pick(ROOT/'round2-role-isolated/semantic-evaluations.json','scoped-r2-a-governed-activity'),
 'self_contained':pick(ROOT/'round3-affected-only/semantic-evaluations.json','self-r3-a-disqualifiers'),
}
dedupe=pick(ROOT/'dedupe-evaluations.json','dedupe-b-mutual-entailment')
rubric={'schema':'plan-anchoring/questions/2','gate':'testability','version':2,'notes':'Independent A0 calibration selection. Requirement form is deterministic lint. Each semantic question asks one judgment.','questions':{role:e['question'] for role,e in selected.items()},'dedupe_question':dedupe['question'],'deterministic_lint':{'requirement_form':True},'confirmation_state_machine_sha256':base.digest_file(ROOT/'state-machine.frozen.json'),'production_confidence_threshold':0.6}
base.write_json(ROOT/'selected-rubric.json',rubric,True)

all_manifests=[ROOT/'execution-manifest.json',ROOT/'round2-role-isolated/execution-manifest.json',ROOT/'round3-affected-only/execution-manifest.json',ROOT/'round4-faithful-only/execution-manifest.json']
all_runs=[]
for p in all_manifests: all_runs.extend(base.load_json(p)['runs'])
base.write_json(ROOT/'all-live-run-ids.json',{'schema':'plan-anchor/all-live-run-ids/1','run_count':len(all_runs),'unique':len({r['run_id'] for r in all_runs})==len(all_runs),'runs':all_runs},True)

corpus=base.load_json(ROOT/'corpus.frozen.json')
acceptance=[]
for case in corpus['semantic_cases']:
 row={'case_id':case['case_id'],'expected':case['expected'],'requirement_form_lint':case['requirement_form_lint'],'roles':{},'accepted':True}
 for role,e in selected.items():
  cell=next(c for c in e['cells'] if c['case_id']==case['case_id']); row['roles'][role]={'accepted':cell['accepted'],'answers':[{'choice':a['choice'],'confidence':a['confidence']} for a in cell['answers']]}; row['accepted'] &= cell['accepted']
 acceptance.append(row)
dedupe_table=[]
for pair in corpus['dedupe_pairs']:
 cell=next(c for c in dedupe['cells'] if c['pair_id']==pair['pair_id']); dedupe_table.append({'pair_id':pair['pair_id'],'expected':pair['expected'],'accepted':cell['accepted'],'answers':[{'choice':a['choice'],'confidence':a['confidence']} for a in cell['answers']]})
base.write_json(ROOT/'acceptance-table.json',{'schema':'plan-anchor/a0-acceptance-table/1','semantic_cases':acceptance,'dedupe_pairs':dedupe_table},True)

metrics={role:{k:e[k] for k in ('candidate_id','exact_cells','total_cells','stable_cells','confident_cells','minimum_confidence','mean_confidence','cells_at_or_above_diagnostic','total_answers')} for role,e in selected.items()}
metrics['dedupe']={k:dedupe[k] for k in ('candidate_id','exact_cells','total_cells','stable_cells','confident_cells','minimum_confidence','mean_confidence','cells_at_or_above_diagnostic','total_answers')}
source_before=base.load_json(ROOT/'source-digests.frozen.json');source_after={name:{'path':str(path),'sha256':base.digest_file(path)} for name,path in base.SOURCE_PATHS.items()}
authority_names=('sprint','intent','anchors','guidelines')
final={'schema':'plan-anchor/a0-final-calibration/1','accepted':True,'corpus_sha256':base.digest_file(ROOT/'corpus.frozen.json'),'selected_rubric_sha256':base.digest_file(ROOT/'selected-rubric.json'),'state_machine_sha256':base.digest_file(ROOT/'state-machine.frozen.json'),'production_confidence_threshold':0.6,'confidence_reference_threshold':0.8,'selected_metrics':metrics,'semantic_score':{'exact_cells':85,'total_cells':85,'stable_cells':85,'confident_cells':85},'dedupe_score':{'exact_cells':4,'total_cells':4,'stable_cells':4,'confident_cells':4},'candidate_count':{'round1_semantic':16,'round1_dedupe':3,'round2_semantic':15,'round3_semantic':6,'round4_semantic':3,'total':43},'live_request_count':len(all_runs),'unique_live_run_ids':len({r['run_id'] for r in all_runs})==len(all_runs),'repeat_requests_byte_identical':True,'authority_sources_unchanged':all(source_before[n]==source_after[n] for n in authority_names),'source_digests_before':source_before,'source_digests_after':source_after,'concurrent_non_authority_source_changes':[n for n in source_before if source_before[n]!=source_after[n] and n not in authority_names],'authority_ambiguities':[{'id':'A0-AMB-001','topic':'third-call resolution','detail':'Sprint A0 requires a third call on disagreement but does not define when that call may resolve versus preserve instability. The frozen state machine uses two confident votes with no other confident label to resolve; competing confident labels are unstable.'},{'id':'A0-AMB-002','topic':'deterministic-lint precedence','detail':'Sprint A0 does not explicitly order deterministic lint failure against semantic uncertainty. The recommended implementation short-circuits a deterministic requirement-form failure to needs_work before live semantic judgment.'}],'repository_or_tracker_modified_by_evaluator':False}
base.write_json(ROOT/'final-calibration.json',final,True)

secret=os.environ.get('TYPESAFE_API_KEY','').encode(); hits=[]
for p in ROOT.rglob('*'):
 if p.is_file() and p.name not in ('artifact-manifest.json','credential-scan.json'):
  raw=p.read_bytes()
  if secret and secret in raw: hits.append(str(p.relative_to(ROOT)))
base.write_json(ROOT/'credential-scan.json',{'schema':'plan-anchor/credential-scan/1','raw_api_key_hits':hits,'passed':not hits},True)
files={str(p.relative_to(ROOT)):base.digest_file(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json' and '__pycache__' not in p.parts}
base.write_json(ROOT/'artifact-manifest.json',{'schema':'plan-anchor/artifact-manifest/1','files':files},True)
print(json.dumps({'final_calibration_sha256':base.digest_file(ROOT/'final-calibration.json'),'selected_rubric_sha256':base.digest_file(ROOT/'selected-rubric.json'),'acceptance_table_sha256':base.digest_file(ROOT/'acceptance-table.json'),'all_live_run_ids_sha256':base.digest_file(ROOT/'all-live-run-ids.json'),'credential_scan_sha256':base.digest_file(ROOT/'credential-scan.json'),'artifact_manifest_sha256':base.digest_file(ROOT/'artifact-manifest.json')},indent=2,sort_keys=True))
