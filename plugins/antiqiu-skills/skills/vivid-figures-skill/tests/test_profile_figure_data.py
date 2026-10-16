"""Behavior checks for the optional, read-only data profiler."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'profile_figure_data.py'
spec = importlib.util.spec_from_file_location('profiler', SCRIPT)
profiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(profiler)


class ProfileTests(unittest.TestCase):
    def test_missing_nonfinite_and_uneven_groups_do_not_mutate_input(self):
        frame = pd.DataFrame({'subject_id': [1, 1, 2, 3, 4], 'group': ['a', 'a', 'a', 'b', None],
                              'score': [1., np.nan, np.inf, 4., -np.inf]})
        before = frame.copy(deep=True)
        report = profiler.profile_dataframe(frame, group='group')
        pd.testing.assert_frame_equal(frame, before)
        score = next(f for f in report['fields'] if f['name'] == 'score')
        self.assertEqual((score['missing'], score['finite_count'], score['nonfinite_count']), (1, 2, 2))
        self.assertEqual(score['numeric']['median'], 2.5)
        self.assertEqual([g['rows'] for g in report['groups']['items']], [3, 1, 1])
        self.assertEqual(report['groups']['items'][0]['valid_by_field']['score']['finite'], 1)
        json.dumps(report, allow_nan=False)

    def test_codes_dates_constants_and_empty_values_are_facts(self):
        frame = pd.DataFrame({'id': [101, 102, 103], 'code': [1, 2, 1], 'constant': [7., 7., 7.],
                              'empty': [None] * 3, 'date': ['2026-01-01', '2026-01-02', '2026-01-03']})
        fields = {f['name']: f for f in profiler.profile_dataframe(frame)['fields']}
        self.assertTrue(fields['id']['all_non_null_values_unique'])
        self.assertTrue(fields['id']['hints'])
        self.assertTrue(fields['code']['hints'])
        self.assertEqual(fields['constant']['numeric']['sample_std'], 0)
        self.assertEqual(fields['empty']['non_null'], 0)
        self.assertNotIn('datetime_range', fields['date'])
        self.assertTrue(fields['date']['hints'])
        empty = profiler.profile_dataframe(pd.DataFrame({'x': pd.Series(dtype='float64')}))
        self.assertEqual(empty['rows'], 0)

    def test_bounds_and_explicit_selection(self):
        frame = pd.DataFrame({f'x{i}': range(30) for i in range(60)})
        report = profiler.profile_dataframe(frame, group='x0')
        self.assertEqual(report['columns_profiled'], 40)
        self.assertEqual(report['requested_columns_omitted'], 20)
        self.assertEqual(report['groups']['omitted'], 10)
        self.assertEqual(profiler.profile_dataframe(frame, columns=['x59'])['fields'][0]['name'], 'x59')
        with self.assertRaises(ValueError):
            profiler.profile_dataframe(frame, columns=['unknown'])

    def test_nullable_numeric_and_categorical_missing_group(self):
        frame = pd.DataFrame({'value': pd.Series([1, None, 3], dtype='Int64'),
                              'group': pd.Categorical(['a', None, 'a'], categories=['a', 'unused'])})
        report = profiler.profile_dataframe(frame, group='group')
        self.assertEqual(report['groups']['total'], 2)
        self.assertEqual(sum(g['rows'] for g in report['groups']['items']), 3)
        json.dumps(report, allow_nan=False)

    def test_csv_tsv_excel_cli_and_input_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            frame = pd.DataFrame({'method': ['A', 'B', 'A'], 'score': [1., 2., 3.]})
            for suffix in ['csv', 'tsv', 'xlsx']:
                source = root / f'data.{suffix}'
                if suffix == 'xlsx':
                    frame.to_excel(source, sheet_name='Results', index=False)
                else:
                    frame.to_csv(source, sep='\t' if suffix == 'tsv' else ',', index=False)
                before = source.read_bytes()
                output = root / 'summary.json'
                command = [sys.executable, '-X', 'utf8', str(SCRIPT), str(source), '--group', 'method', '--output', str(output)]
                if suffix == 'xlsx':
                    command += ['--sheet', 'Results']
                subprocess.run(command, check=True, capture_output=True)
                report = json.loads(output.read_text(encoding='utf-8'))
                self.assertEqual(report['rows'], 3)
                self.assertEqual(source.read_bytes(), before)
                blocked = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output', str(source)], capture_output=True)
                self.assertNotEqual(blocked.returncode, 0)
                self.assertEqual(source.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
