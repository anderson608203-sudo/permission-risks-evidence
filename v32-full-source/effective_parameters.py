"""Versioned finite limits; no sample-specific overrides."""
import json
from pathlib import Path
from functools import lru_cache
@lru_cache(maxsize=1)
def current():
    data=json.loads((Path(__file__).resolve().parents[2]/'configs/method_evidence.r1.json').read_text(encoding='utf8'))
    v=data['effective_parameters'];assert v['normalization_visits_per_operation_max'] in (100000,150000,200000)
    assert v['max_source_paths']==data['P']['max_source_paths']
    fixed={'expression_nodes_max':50000,'expression_depth_max':100,'expression_string_bytes_max':1048576,
        'expression_key_characters_max':262144,'source_evaluations_per_operation_max':2048,'call_depth_max':8,
        'solver_timeout_ms':3000,'variable_loop_frontier':2,'constant_loop_max':32}
    assert all(v[k]==x for k,x in fixed.items()),'UNVALIDATED_FINITE_PARAMETER_CHANGE'
    return {**v,'solver_timeout_upgrade_ms':10000,'solver_sample_seconds':120,'external_sequence_max':3,'dependency_closure_nodes_max':4096,'sequence_checks_per_sample_max':24,'sequence_paths_per_stage_max':8}
