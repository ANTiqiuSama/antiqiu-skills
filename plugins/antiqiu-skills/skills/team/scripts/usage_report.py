"""Summarize measured task tokens and provider-specific quota; never query a model."""
import argparse
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path


def tokens_b(tokens):
    if tokens is None:
        return None
    if isinstance(tokens, bool) or not isinstance(tokens, int) or tokens < 0:
        raise ValueError('total_tokens must be a nonnegative integer or null')
    rounded = (Decimal(tokens) / Decimal(1_000_000_000)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    return format(rounded, '.1f') if rounded else None


def summarize(data):
    unique = {}
    for record in data.get('records', []):
        key = record['measurement_id']
        if not key or not record.get('source') or not record.get('provider'):
            raise ValueError('measurement_id, source and provider are required')
        tokens_b(record.get('total_tokens'))
        if key in unique and unique[key] != record:
            raise ValueError('conflicting measurement: ' + key)
        unique[key] = record
    rows = list(unique.values())
    known = [r['total_tokens'] for r in rows if r.get('total_tokens') is not None]
    used = {p.lower() for p in data.get('used_providers', [])}
    used.update(r['provider'].lower() for r in rows)
    notices = []
    for provider in sorted(used & {'grok', 'gemini', 'codex'}):
        samples = [q for q in data.get('quotas', []) if q['provider'].lower() == provider]
        if not samples:
            notices.append({'provider': provider, 'status': 'unknown'})
        for q in samples:
            rem = q.get('remaining_percent')
            if rem is None and q.get('used_percent') is not None:
                used_pct = q['used_percent']
                if isinstance(used_pct, bool) or not isinstance(used_pct, (int, float)):
                    raise ValueError('used_percent must be numeric')
                rem = max(0, min(100, 100 - used_pct))
            if rem is not None and (isinstance(rem, bool) or not isinstance(rem, (int, float)) or not 0 <= rem <= 100):
                raise ValueError('remaining_percent must be between 0 and 100')
            if rem is None or rem < 30:
                notices.append({**q, 'status': 'unknown' if rem is None else 'low', 'remaining_percent': rem})
    represented = {r['provider'].lower() for r in rows}
    return {
        'measured_total_tokens': sum(known) if known else None,
        'measured_total_B': tokens_b(sum(known)) if known else None,
        'report_tokens': bool(known) and tokens_b(sum(known)) is not None,
        'complete': bool(rows) and len(known) == len(rows) and used <= represented
                    and not any(r.get('scope') == 'session_cumulative_no_baseline' for r in rows),
        'records': rows,
        'quota_notices': notices,
    }


def codex_measurement(path, request_text):
    latest = None
    baseline = None
    found = False
    start = None
    with Path(path).open(encoding='utf-8') as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                if stream.read().strip():
                    raise ValueError('corrupt usage log before its final line')
                break  # An actively written final line can be incomplete.
            payload = event.get('payload', {})
            if event.get('type') == 'response_item' and payload.get('role') == 'user':
                text = '\n'.join(c.get('text', '') for c in payload.get('content', []) if isinstance(c, dict))
                if request_text in text:
                    if found:
                        raise ValueError('request_text matches more than one user message')
                    baseline, start, found = latest, event.get('timestamp'), True
            if payload.get('type') == 'token_count' and payload.get('info'):
                usage = payload['info'].get('total_token_usage')
                if usage and 'total_tokens' in usage:
                    latest = (event.get('timestamp'), usage['total_tokens'])
    if not found or latest is None:
        raise ValueError('request or token usage was not found')
    task_scope = baseline is not None
    total = latest[1] - baseline[1] if task_scope else latest[1]
    tokens_b(total)  # A counter reset must not silently become a valid delta.
    return {
        'measurement_id': str(Path(path).resolve()) + ':' + str(start),
        'provider': 'codex', 'total_tokens': total,
        'scope': 'task_delta' if task_scope else 'session_cumulative_no_baseline',
        'source': str(Path(path).resolve()), 'as_of': latest[0],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--input', type=Path)
    source.add_argument('--codex-session', type=Path)
    parser.add_argument('--request-text')
    args = parser.parse_args()
    if args.codex_session:
        if not args.request_text:
            parser.error('--request-text is required with --codex-session')
        data = {'records': [codex_measurement(args.codex_session, args.request_text)]}
    else:
        data = json.loads(args.input.read_text(encoding='utf-8'))
    print(json.dumps(summarize(data), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
