"""Retired variable-only binder. Immutable original remains in source_snapshot_51d1bc9ad06a.
Current production uses completion.construct_candidates and relations/policies.
"""
from .core import Invalid

def bind_draft(*args, **kwargs):
    raise Invalid('legacy_binding_retired_use_key_aware_completion_pipeline')
