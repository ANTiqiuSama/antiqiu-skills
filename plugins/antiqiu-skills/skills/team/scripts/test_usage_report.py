import json
from pathlib import Path
import tempfile
import unittest

from usage_report import codex_measurement, summarize, tokens_b


def row(n=1100, provider='grok', identity='request-1'):
    return {'measurement_id': identity, 'provider': provider, 'total_tokens': n, 'source': 'fixture-receipt'}


class UsageTests(unittest.TestCase):
    def test_B_display_uses_one_decimal(self):
        self.assertEqual(tokens_b(1_000_000_000), '1.0')
        self.assertEqual(tokens_b(1_260_000_000), '1.3')

    def test_tiny_usage_is_suppressed(self):
        for count in [0, 1, 40_533, 4_833_628, 49_999_999]:
            with self.subTest(count=count):
                result = summarize({'records': [row(count)]})
                self.assertIsNone(result['measured_total_B'])
                self.assertFalse(result['report_tokens'])
                self.assertEqual(result['measured_total_tokens'], count)

    def test_rounding_boundary_is_half_up(self):
        self.assertEqual(tokens_b(50_000_000), '0.1')
        self.assertEqual(tokens_b(150_000_000), '0.2')

    def test_small_usage_does_not_hide_low_quota(self):
        result = summarize({'records': [row(1100)], 'quotas': [{'provider': 'grok', 'remaining_percent': 29}]})
        self.assertFalse(result['report_tokens'])
        self.assertEqual(result['quota_notices'][0]['status'], 'low')

    def test_inclusive_subcounts_are_not_added(self):
        record = {**row(), 'input_tokens': 1000, 'cached_input_tokens': 800, 'output_tokens': 100, 'reasoning_output_tokens': 40}
        self.assertEqual(summarize({'records': [record]})['measured_total_tokens'], 1100)

    def test_identical_receipt_is_counted_once(self):
        self.assertEqual(summarize({'records': [row(), row()]})['measured_total_tokens'], 1100)

    def test_conflicting_receipt_rejected(self):
        with self.assertRaises(ValueError):
            summarize({'records': [row(), row(1200)]})

    def test_unknown_tokens_are_not_zero(self):
        result = summarize({'records': [row(None)]})
        self.assertIsNone(result['measured_total_B'])
        self.assertFalse(result['complete'])

    def test_partial_and_unrepresented_providers(self):
        result = summarize({'records': [row()], 'used_providers': ['grok', 'gemini']})
        self.assertFalse(result['complete'])
        self.assertEqual(len(result['quota_notices']), 2)

    def test_quota_threshold_is_strict(self):
        for remaining, count in [(29.999, 1), (30, 0), (75, 0), (0, 1)]:
            with self.subTest(remaining=remaining):
                result = summarize({'records': [row()], 'quotas': [{'provider': 'grok', 'window': '5h', 'remaining_percent': remaining}]})
                self.assertEqual(len(result['quota_notices']), count)

    def test_supplier_and_window_separation(self):
        result = summarize({'records': [row()], 'quotas': [
            {'provider': 'codex', 'remaining_percent': 1},
            {'provider': 'gemini', 'remaining_percent': 2},
            {'provider': 'grok', 'window': 'short', 'remaining_percent': 60},
            {'provider': 'grok', 'window': 'weekly', 'used_percent': 81}]})
        self.assertEqual(len(result['quota_notices']), 1)
        self.assertEqual(result['quota_notices'][0]['remaining_percent'], 19)
        self.assertEqual(result['quota_notices'][0]['window'], 'weekly')

    def test_unknown_quota_is_reported(self):
        result = summarize({'records': [row()]})
        self.assertEqual(result['quota_notices'], [{'provider': 'grok', 'status': 'unknown'}])

    def test_invalid_counts_fail(self):
        for value in [-1, True, 1.5]:
            with self.assertRaises(ValueError):
                tokens_b(value)

    def session(self, totals, baseline=True):
        events = []
        def usage(n, at):
            return {'timestamp': at, 'payload': {'type': 'token_count', 'info': {'total_token_usage': {'total_tokens': n}}}}
        if baseline:
            events.append(usage(900, 'before'))
        events.append({'timestamp': 'start', 'type': 'response_item', 'payload': {'role': 'user', 'content': [{'text': 'unique synthetic task'}]}})
        events.extend(usage(n, str(i)) for i, n in enumerate(totals))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'session.jsonl'
            path.write_text('\n'.join(json.dumps(e) for e in events) + '\n{"partial":', encoding='utf-8')
            return codex_measurement(path, 'unique synthetic task')

    def test_cumulative_snapshots_use_delta(self):
        result = self.session([1000, 1100, 1100])
        self.assertEqual(result['total_tokens'], 200)
        self.assertEqual(result['scope'], 'task_delta')

    def test_no_baseline_is_disclosed(self):
        result = self.session([1100], baseline=False)
        self.assertEqual(result['scope'], 'session_cumulative_no_baseline')
        self.assertFalse(summarize({'records': [result]})['complete'])

    def test_counter_reset_is_not_fabricated_delta(self):
        with self.assertRaises(ValueError):
            self.session([100])


if __name__ == '__main__':
    unittest.main()
