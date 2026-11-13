"""Local-only DeepSeek HTTPS client. Credential never leaves Authorization memory.

R4.1 adds an explicit batch binding. C2 clients read C1 as history but write
only their own C2 ledger/proposals; the C1 ledger is never opened for append.
"""
import contextlib, datetime, decimal, hashlib, json, os, pathlib, time, urllib.error, urllib.request, uuid
from .core import require, canonical, digest, Invalid
from .llm_transport import read_response
from .llm_stream import read_stream,stream_request
from .llm_limits import (POLICY_ID, PROVIDER_CONTEXT_TOKENS, RESPONSE_MAX_BYTES,
                         output_estimate)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise urllib.error.HTTPError(args[0].full_url, 399, 'redirect_rejected', None, None)

class Client:
    C1_BASELINE_SHA256 = '3e6aa8a20a63f70b03480fbf378bc7ff57e4f1a6fe49b7bb1c5063d9624062ac'

    def __init__(self, root, batch=None, history_ledgers=None, proposal_dir=None, history_identity=None, simulated=False, history_identities=None):
        self.root = pathlib.Path(root)
        self.batch = pathlib.Path(batch) if batch else self.root / 'batches/c1_20261017_r1'
        self.batch_ref = self.batch.relative_to(self.root).as_posix()
        self.simulated = bool(simulated)
        self.source_nature = 'simulated' if self.simulated else 'real'
        self.ledger = self.batch / 'RESOURCE_LEDGER.jsonl'
        self.history_ledgers = [pathlib.Path(p) for p in (history_ledgers or []) if pathlib.Path(p) != self.ledger]
        self.history_identity = history_identity
        self.history_identities = {str(pathlib.Path(k)): v for k, v in (history_identities or {}).items()}
        self.proposal_dir = pathlib.Path(proposal_dir) if proposal_dir else self.batch / 'completion_proposals'
        c1_batch = (self.root / 'batches/c1_20261017_r1').resolve()
        self.is_c2 = self.batch.resolve() != c1_batch
        if self.is_c2:
            require(self.history_ledgers, 'C1_HISTORY_REQUIRED')
            for path in self.history_ledgers:
                require(path.exists(), 'HISTORY_LEDGER_MISSING:' + str(path))
            require(self.history_identity, 'C1_HISTORY_IDENTITY_REQUIRED')
            require(self.history_identity == self.C1_BASELINE_SHA256, 'C1_HISTORY_IDENTITY_NOT_APPROVED')
            for path in self.history_ledgers:
                expected = self.history_identities.get(str(path), self.history_identity)
                require(expected is not None and hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'C1_HISTORY_IDENTITY_MISMATCH:' + str(path))
        self.price = json.loads((self.root / 'configs/deepseek_pricing.json').read_text(encoding='utf-8'))

    def append(self, item):
        parallel=getattr(self,'parallel_reservations',False)
        budget_fd=None
        if parallel:
            import fcntl
            # Reservation already holds this mutex. Settlement changes the
            # amount available to the next admission and uses the same mutex.
            if item.get('event')=='api_settled':
                budget_fd=os.open(self.batch/'api_budget.lock',os.O_CREAT|os.O_WRONLY,0o600)
                fcntl.flock(budget_fd,fcntl.LOCK_EX)
        try:
            with self.ledger.open('a', encoding='utf-8') as f:
                if parallel:fcntl.flock(f,fcntl.LOCK_EX)
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                f.flush(); os.fsync(f.fileno())
        finally:
            if budget_fd is not None:os.close(budget_fd)

    def _rows(self, path, required=False):
        if not path.exists():
            require(not required, 'HISTORY_LEDGER_MISSING:' + str(path))
            return []
        with path.open(encoding='utf8') as f:
            if getattr(self,'parallel_reservations',False):
                import fcntl
                fcntl.flock(f,fcntl.LOCK_SH)
            return [json.loads(line) for line in f.read().splitlines() if line.strip()]

    def budget_snapshot(self):
        """Cumulative C1+C2 budget view; current ledger is counted once."""
        reservations, settles = {}, {}
        paths = []
        for path in self.history_ledgers + [self.ledger]:
            if path not in paths:
                paths.append(path)
        for path in paths:
            expected = self.history_identities.get(str(path), self.history_identity)
            if path in self.history_ledgers and expected is not None:
                require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'C1_HISTORY_IDENTITY_MISMATCH:' + str(path))
            for row in self._rows(path, required=path in self.history_ledgers):
                if row.get('event') == 'api_reserved':
                    old = reservations.get(row['request_id'])
                    if old is not None:
                        require(all(old.get(k) == row.get(k) for k in ['input_tokens', 'output_tokens', 'cost_usd', 'request_sha256']), 'CONFLICTING_API_RESERVATION')
                    reservations[row['request_id']] = row
                elif row.get('event') == 'api_settled':
                    old = settles.get(row['request_id'])
                    if old is not None:
                        require(all(old.get(k) == row.get(k) for k in ['input_tokens', 'output_tokens', 'cost_usd']), 'CONFLICTING_API_SETTLEMENT')
                    settles[row['request_id']] = row
        require(not (set(settles) - set(reservations)), 'API_SETTLEMENT_WITHOUT_RESERVATION')
        inp = out = 0
        cost = decimal.Decimal('0')
        for rid, reserved in reservations.items():
            settled = settles.get(rid, reserved)
            inp += settled['input_tokens']; out += settled['output_tokens']
            cost += decimal.Decimal(settled['cost_usd'])
        return {'attempts': len(reservations), 'input_tokens': inp, 'output_tokens': out,
                'cost_usd_upper': str(cost), 'unsettled_requests': sorted(set(reservations) - set(settles)),
                'ledgers': [str(p) for p in paths]}

    def check_budget(self, input_bound, max_tokens, reasoning_effort='high', request_count=1):
        usage = self.budget_snapshot()
        require(type(input_bound) is int and input_bound > 0 and type(request_count) is int and request_count > 0,
                'budget_estimate_shape')
        # An omitted request limit uses a provider-default ESTIMATE for accounting.
        # The API receives no max_tokens field. Actual usage always wins at settlement.
        output_bound = output_estimate(None, reasoning_effort) * request_count if max_tokens is None else max_tokens
        require(type(output_bound) is int and output_bound > 0, 'budget_estimate_shape')
        pi = decimal.Decimal(self.price['input_usd_per_million_max'])
        po = decimal.Decimal(self.price['output_usd_per_million_max'])
        reserve = (pi * input_bound + po * output_bound) / 1000000
        token_ok = self.is_c2 or (usage['input_tokens'] + input_bound <= 200000 and
                                  usage['output_tokens'] + output_bound <= 40000)
        require(usage['attempts'] + request_count <= 40 and token_ok and
                decimal.Decimal(usage['cost_usd_upper']) + reserve <= 10, 'api_cumulative_budget')
        require(not usage['unsettled_requests'], 'api_unsettled_request_requires_reconciliation')
        return usage, reserve

    def batch_binding(self):
        c1 = self.root / 'batches/c1_20261017_r1/RESOURCE_LEDGER.jsonl'
        c2 = self.root / 'batches/c2_20261017_r1/RESOURCE_LEDGER.jsonl'
        return {'batch': self.batch_ref,
                'c1_ledger_sha256': hashlib.sha256(c1.read_bytes()).hexdigest(),
                'c2_ledger_sha256': hashlib.sha256(c2.read_bytes()).hexdigest(),
                'budget': self.budget_snapshot()}

    def call(self, messages, label, max_tokens=4096, timeout=120, reasoning_effort='high', thinking=True):
        require(type(timeout) in (int, float) and 0 < timeout <= (1800 if self.is_c2 else 120), 'request_limits')
        if not self.is_c2:
            require(type(max_tokens) is int and 1 <= max_tokens <= 4096, 'request_limits')
        output_bound = output_estimate(max_tokens, reasoning_effort)
        require(all(set(m) == {'role', 'content'} and m['role'] in ['system', 'user'] and isinstance(m['content'], str) for m in messages), 'message_format')
        require('json' in ''.join(m['content'] for m in messages).lower(), 'json_instruction')
        # UTF-8 bytes dominate byte-level tokenization; 512 additionally reserves framing.
        input_bound = len(canonical(messages)) + 512
        if self.is_c2:
            require(input_bound + output_bound <= PROVIDER_CONTEXT_TOKENS, 'provider_context_upper_bound')
        else:
            require(input_bound <= 10000, 'input_token_upper_bound')
        require(reasoning_effort in ['high', 'low', 'none'], 'unapproved_effort')
        require(thinking == (reasoning_effort != 'none'), 'mode_effort_mismatch')
        request = {'model': 'deepseek-flash', 'messages': messages, 'response_format': {'type': 'json_object'},
                   'thinking': {'type': 'enabled' if thinking else 'disabled'}, 'reasoning_effort': reasoning_effort,
                   'max_tokens': max_tokens, 'stream': False}
        if max_tokens is None:
            del request['max_tokens']
        transport=getattr(self,'transport_mode','json_v1')
        require(transport in ('json_v1','sse_v1'),'unapproved_transport')
        semantic_identity=digest(request)
        if transport=='sse_v1':request=stream_request(request)
        transport_identity=({'semantic_request_sha256':semantic_identity,'request_transport':transport}
                            if transport=='sse_v1' else {})
        lock = self.batch / 'api_budget.lock'
        parallel=getattr(self,'parallel_reservations',False)
        if parallel:
            import fcntl
            fd=os.open(lock,os.O_CREAT|os.O_WRONLY,0o600);fcntl.flock(fd,fcntl.LOCK_EX)
        else:fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        try:
            usage, reserve = self.check_budget(input_bound, max_tokens, reasoning_effort=reasoning_effort)
            # Credentials and HTTP request construction must succeed before reserving.
            # Never log credential contents or exception messages containing headers.
            secret = pathlib.Path(getattr(self,'credential_file',self.root/'deepseek.txt')).read_text(encoding='utf-8').strip()
            require(secret and '\n' not in secret and '\r' not in secret, 'credential_format')
            req = urllib.request.Request('https://api.deepseek.com/chat/completions', data=canonical(request),
                                         headers={'Authorization': 'Bearer ' + secret, 'Content-Type': 'application/json'},
                                         method='POST')
            del secret
            opener = urllib.request.build_opener(NoRedirect())
            rid = uuid.uuid4().hex
            self.append({**transport_identity, 'event': 'api_reserved', 'request_id': rid, 'label': label,
                         **({'worker_pid':os.getpid(),'worker_start_token':pathlib.Path('/proc/self/stat').read_text().split()[21],'reserved_epoch':time.time()} if parallel else {}),
                         'input_tokens': input_bound, 'output_tokens': output_bound, 'cost_usd': str(reserve),
                         'output_reservation_kind': 'provider_default_estimate' if max_tokens is None else 'explicit_request_limit',
                         'token_budget_policy': POLICY_ID if self.is_c2 else 'legacy_c1',
                         'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         'request_sha256': digest(request), 'batch': self.batch_ref, 'simulated': self.simulated, 'source_nature': self.source_nature})
            dest = self.batch / 'api' / rid
            dest.mkdir(parents=True, exist_ok=False)
            (dest / 'request.json').write_bytes(canonical(request))
            start = time.monotonic()
            receipt = {**transport_identity, 'request_id': rid, 'label': label, 'request_sha256': digest(request),
                       'model_requested': 'deepseek-flash', 'reasoning_effort': reasoning_effort,
                       'reasoning_content_saved': False, 'reserved_cost_usd': str(reserve),
                       'request_max_tokens': max_tokens, 'request_max_tokens_omitted': max_tokens is None,
                       'output_tokens_estimate': output_bound, 'timeout_seconds': timeout,
                       'response_max_bytes': RESPONSE_MAX_BYTES,
                       'token_budget_policy': POLICY_ID if self.is_c2 else 'legacy_c1',
                       'batch': self.batch_ref, 'simulated': self.simulated, 'source_nature': self.source_nature}
            receipt.update(dispatch_started=False, failure_phase='before_dispatch')
            if parallel:fcntl.flock(fd,fcntl.LOCK_UN)
            try:
                # Crossing this marker makes transport failures uncertain, never free.
                self.append({'event': 'api_dispatch_started', 'request_id': rid,
                             'request_sha256': digest(request), 'batch': self.batch_ref,
                             'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                             'simulated': self.simulated, 'source_nature': self.source_nature})
                receipt['dispatch_started'] = True
                receipt['failure_phase'] = 'http_request_or_response'
                with opener.open(req, timeout=timeout) as response:
                    receipt['http_response'] = {}
                    if transport=='sse_v1':
                        data=read_stream(response,RESPONSE_MAX_BYTES,receipt['http_response'],
                                         deadline=start+timeout,partial_path=dest/'partial_final_content.txt')
                    else:
                        data = read_response(response, RESPONSE_MAX_BYTES, receipt['http_response'],
                                             deadline=start + timeout)
                del req
                used = data.get('usage', {}); tokens_in = used.get('prompt_tokens'); tokens_out = used.get('completion_tokens')
                require(type(tokens_in) is int and type(tokens_out) is int and tokens_in >= 0 and tokens_out >= 0, 'missing_usage')
                usage_clean = {k: v for k, v in used.items() if type(v) is int}
                details = used.get('completion_tokens_details', {})
                if isinstance(details, dict) and type(details.get('reasoning_tokens')) is int:
                    usage_clean['reasoning_tokens'] = details['reasoning_tokens']
                receipt.update(model_returned=data.get('model'), usage=usage_clean, provider_id=data.get('id'),
                               system_fingerprint=data.get('system_fingerprint'))
                actual_ceiling = (decimal.Decimal(self.price['input_usd_per_million_max']) * tokens_in +
                                  decimal.Decimal(self.price['output_usd_per_million_max']) * tokens_out) / 1000000
                self.append({'event': 'api_settled', 'request_id': rid, 'input_tokens': tokens_in,
                             'output_tokens': tokens_out, 'cost_usd': str(actual_ceiling),
                             'cost_kind': 'usage_at_official_max_rate_upper_bound', 'usage': usage_clean,
                             'batch': self.batch_ref, 'simulated': self.simulated, 'source_nature': self.source_nature})
                c = data['choices'][0]; text = c['message'].get('content', ''); finish = c.get('finish_reason')
                receipt['finish_reason'] = finish
                receipt['final_content_characters'] = len(text) if isinstance(text, str) else 0
                receipt['json_parse_attempted'] = False
                receipt['output_estimate_exceeded'] = tokens_out > output_bound
                # Preserve the received final text even if JSON parsing fails.
                # Never persist credentials/HTTP headers or hidden reasoning.
                if isinstance(text, str):
                    (dest / 'final_content_raw.txt').write_bytes(text.encode('utf-8'))
                    receipt['raw_final_content_sha256'] = hashlib.sha256(text.encode('utf-8')).hexdigest()
                del data
                require(finish == 'stop', 'truncated_or_incomplete_output')
                require(isinstance(text, str) and bool(text.strip()), 'empty_output')
                receipt['json_parse_attempted'] = True
                from .m08_protocol import parse_text
                content,normalizations = parse_text(text)
                require(isinstance(content, dict), 'output_not_object')
                receipt['format_normalizations'] = normalizations
                (dest / 'final_content.json').write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding='utf-8')
                receipt['response_sha256'] = digest(content)
                receipt['status'] = 'json_received'
                receipt['failure_phase'] = None
            except urllib.error.HTTPError as error:
                receipt.update(status='http_error', http_status=error.code); content = None
            except Invalid as error:
                receipt.update(status=str(error), error_class=type(error).__name__); content = None
            except Exception as error:
                receipt.update(status='request_failed', error_class=type(error).__name__); content = None
            receipt['elapsed_seconds'] = time.monotonic() - start
            (dest / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
            self.append({'event': 'api_returned', **receipt})
            return content, receipt
        finally:
            os.close(fd)
            if not parallel:lock.unlink()
