"""Regression tests for review hints, not a claim of visual correctness."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/review_recipe_style.py'
spec = importlib.util.spec_from_file_location('review', SCRIPT)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


def source(tid):
    cards=json.loads((ROOT/'catalog/cards.json').read_text(encoding='utf8'))['cards']
    card=next(c for c in cards if c['id']==tid)
    return (ROOT/'catalog'/card['source']['original_code']).read_text(encoding='utf8')


class StyleTests(unittest.TestCase):
    def test_appended_data_does_not_hide_drawing_loop(self):
        original = 'groups=[]\nfor x in data:\n groups.append(x)\nfor g in groups:\n ax.fill_between(t,0,g,alpha=.6)\n'
        records = review.inspect_source(original)
        self.assertTrue(any(r['method']=='fill_between' for r in records))
        changed = original.replace('ax.fill_between(t,0,g,alpha=.6)', 'pass')
        self.assertTrue(any(f['kind']=='operation_not_found' for f in review.compare_sources(original,changed)['findings']))

    def test_plotly_transparency_and_missing_trace_are_detected(self):
        original = 'fig=go.Figure(go.Volume(x=x,y=y,z=z,value=v,opacity=.1,surface_count=25))'
        changed = original.replace('opacity=.1','opacity=1')
        self.assertTrue(any(f.get('parameter')=='opacity' for f in review.compare_sources(original,changed)['findings']))
        self.assertTrue(any(f['kind']=='operation_not_found' for f in review.compare_sources(original,'fig=go.Figure()')['findings']))

    def test_real_opacity_order_regression(self):
        # Reduced from the weekly bootstrap plot: bounds changed legitimately,
        # while the outer band's opacity was accidentally reversed.
        original = source('basic.line')
        adapted = original.replace('enumerate([0.15, 0.08, 0.03])', 'enumerate([0.03, 0.08, 0.15])')
        self.assertNotEqual(original, adapted)
        found = review.compare_sources(original, adapted)['findings']
        self.assertTrue(any(f.get('parameter') == 'alpha' and f['kind'] == 'style_changed' for f in found))
        self.assertFalse(review.compare_sources(original, original)['findings'])

    def test_data_bounds_labels_size_and_color_are_adaptable(self):
        original = 'for level, a in [(95,.15),(80,.08),(50,.03)]:\n ax.fill_between(x, low[level], high[level], alpha=a, color=palette[i])\n'
        changed = 'for level, a in [(95,.15),(80,.08),(50,.03)]:\n ax.fill_between(weeks, actual_low[level], actual_high[level], alpha=a, color=bluepink[i])\nax.set_ylabel("New units")\nfig.set_size_inches(8,5)\n'
        findings = review.compare_sources(original, changed)['findings']
        self.assertTrue(findings)
        self.assertTrue(all(f['severity'] == 'advisory' and f['method'] == 'set_size_inches' for f in findings))

    def test_group_repetition_is_not_a_changed_style(self):
        original = 'for group in [1,2,3]:\n ax.scatter(x[group],y[group],alpha=.4,edgecolor="white")\n'
        changed = 'for group in current_groups:\n ax.scatter(x[group],y[group],alpha=.4,edgecolor="white")\n'
        found = review.compare_sources(original, changed)['findings']
        self.assertEqual({f['kind'] for f in found}, {'repetition_changed'})
        # Repeating transparent layers can change appearance, so keep an advisory.
        self.assertTrue(found)

    def test_removed_layer_and_nested_outline(self):
        for tid, before, after, kind in [
            ('basic.raincloud','range(6)','range(1)','style_changed'),
            ('advanced.grouped_violin','pc.set_alpha(0.8)','pc.set_alpha(1.0)','style_changed'),
            ('competition.correlation_matrix','annot=True','annot=False','style_changed'),
            ('competition.surface_3d','alpha=0.85','alpha=1.0','style_changed'),
            ('basic.raincloud','edgecolor=PALETTE[i], linewidth=1.2','edgecolor="none", linewidth=0','unresolved')]:
            with self.subTest(tid=tid,before=before):
                original=source(tid); changed=original.replace(before,after)
                self.assertNotEqual(original,changed)
                self.assertTrue(any(f['kind']==kind for f in review.compare_sources(original,changed)['findings']))

    def test_palette_and_range_differences_are_informational(self):
        before='ax.imshow(values,cmap="coolwarm",vmin=-1,vmax=1)'
        after='ax.imshow(values,cmap="PiYG",vmin=-2,vmax=2)'
        found=review.compare_sources(before,after)['findings']
        self.assertEqual({f['kind'] for f in found},{'palette_changed','data_mapping_changed'})

    def test_dynamic_color_does_not_hide_known_opacity(self):
        original=source('advanced.funnel')
        changed=original.replace("PALETTE[2], 0.06", "PALETTE[2], 0.6")
        found=review.compare_sources(original,changed)['findings']
        self.assertTrue(any(f.get('parameter')=='alpha' and f['kind']=='style_changed' for f in found))
        json.dumps(review.inspect_source('ax.contour(x,y,z,levels=[unknown,1])'))

    def test_patch_and_lightening_changes(self):
        for tid,before,after in [('advanced.sankey','alpha=0.42','alpha=1.0'),
                                 ('advanced.ridgeline','_lighten(color, 0.5)','_lighten(color, 0.0)')]:
            original=source(tid)
            self.assertTrue(any(f['kind']=='style_changed' for f in review.compare_sources(original,original.replace(before,after))['findings']))

    def test_unknown_helpers_and_no_candidate_execution(self):
        before='ax.fill_between(x,lo,hi,alpha=.2)'
        changed='render_band(ax,x,lo,hi)\nraise RuntimeError("must not execute")'
        self.assertEqual(review.compare_sources(before,changed)['findings'][0]['kind'],'operation_not_found')
        unresolved=review.compare_sources(before,'ax.fill_between(x,lo,hi,alpha=get_alpha())')['findings']
        self.assertEqual(unresolved[0]['kind'],'unresolved')
        # Same expression does not prove the same value at runtime.
        self.assertIn('不执行代码',review.compare_sources(before,before)['limits'])

    def test_all_catalog_sources_parse_and_unchanged_has_no_findings(self):
        cards=json.loads((ROOT/'catalog/cards.json').read_text(encoding='utf8'))['cards']
        for card in cards:
            with self.subTest(tid=card['id']):
                original=source(card['id'])
                self.assertFalse(review.compare_sources(original,original)['findings'])

    def test_cli_input_protection_parse_error_and_advisory_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'candidate.py'; path.write_text('ax.plot(x,y)',encoding='utf8')
            command=[sys.executable,str(SCRIPT),'--id','basic.line','--candidate',str(path)]
            completed=subprocess.run(command,capture_output=True,encoding='utf8')
            self.assertEqual(completed.returncode,0)
            self.assertTrue(json.loads(completed.stdout)['findings'])
            before=path.read_bytes()
            blocked=subprocess.run(command+['--output',str(path)],capture_output=True)
            self.assertNotEqual(blocked.returncode,0); self.assertEqual(before,path.read_bytes())
            path.write_text('def broken(',encoding='utf8')
            self.assertNotEqual(subprocess.run(command,capture_output=True).returncode,0)


if __name__ == '__main__': unittest.main()
