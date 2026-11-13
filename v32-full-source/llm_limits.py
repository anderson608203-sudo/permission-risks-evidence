"""Versioned provider metadata; estimates are not project token spending caps.

Source: https://api-docs.deepseek.com/api/create-chat-completion/
and /quick_start/pricing/, checked 2026-10-19. Not a live provider guarantee.
User policy: DECISION_LLM_TOKEN_POLICY_AMENDMENT_R1/USER_DECISION.json.
"""
from .core import require

POLICY_ID = 'c2-user-token-monitor-only-20261019-r1'
PROVIDER_CONTEXT_TOKENS = 1048576
PROVIDER_MAX_OUTPUT_TOKENS = 393216
PROVIDER_THINKING_DEFAULT = 65536
PROVIDER_NONTHINKING_DEFAULT = 8192
RESPONSE_MAX_BYTES = 16 * 1024 * 1024
PROVIDER_DEFAULT_CALL_POLICY = {
    'schema': 'joint-provider-default-call-v1', 'policy_id': POLICY_ID,
    'output_mode': 'provider_default', 'token_budget_mode': 'monitor_only',
    'timeout_seconds': 1800, 'estimated_provider_output_tokens': PROVIDER_THINKING_DEFAULT,
    'provider_context_tokens': PROVIDER_CONTEXT_TOKENS, 'response_max_bytes': RESPONSE_MAX_BYTES,
}

def output_estimate(max_tokens, reasoning_effort='high'):
    require(reasoning_effort in ('high', 'low', 'none'), 'unapproved_effort')
    if max_tokens is None:
        return PROVIDER_NONTHINKING_DEFAULT if reasoning_effort == 'none' else PROVIDER_THINKING_DEFAULT
    require(type(max_tokens) is int and 1 <= max_tokens <= PROVIDER_MAX_OUTPUT_TOKENS, 'request_output_limit')
    return max_tokens

def validate_default_policy(value):
    require(isinstance(value, dict) and value == PROVIDER_DEFAULT_CALL_POLICY,
            'joint_provider_default_policy_identity')
    require(type(value['timeout_seconds']) is int and type(value['estimated_provider_output_tokens']) is int,
            'joint_provider_default_policy_types')
    return value
