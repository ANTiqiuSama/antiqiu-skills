"""Check usable source/preview references and controlled omission hints across the catalog."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'catalog'
CARDS=json.loads((CATALOG/'cards.json').read_text(encoding='utf8'))['cards']


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


review=load('review',ROOT/'scripts/review_recipe_style.py')


class CatalogTests(unittest.TestCase):
    def test_source_hashes_and_checkpoint_links_and_snippets(self):
        page=(CATALOG/'index.html').read_text(encoding='utf8')
        for card in CARDS:
            with self.subTest(tid=card['id']):
                source=CATALOG/card['source']['original_code']
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),card['source']['code_sha256'])
                lines=source.read_text(encoding='utf8').splitlines()
                self.assertTrue(card['fidelity_checkpoints'])
                md=(CATALOG/card['card_path']).read_text(encoding='utf8')
                for point in card['fidelity_checkpoints']:
                    self.assertTrue(point['preserve']);self.assertTrue(point['allowed_adaptation'])
                    self.assertTrue(point['evidence'])
                    for e in point['evidence']:
                        self.assertEqual(e['code'],'\n'.join(lines[e['line']-1:e['end_line']]))
                        self.assertIn(e['href'],page);self.assertIn(e['href'],md)
                        file,anchor=e['href'].split('#')
                        self.assertIn(f'id="{anchor}"',(CATALOG/file).read_text(encoding='utf8'))

    def test_current_recipe_main_blocks_match_catalog(self):
        module=load('recipes',ROOT/'original/resources/assets/shared-scripts/get_recipe.py')
        recipes=module.Recipes(ROOT/'original/resources/assets/shared-scripts')
        for card in CARDS:
            with self.subTest(tid=card['id']):
                if card['id']=='template.sem_violin_pearson':
                    self.assertEqual((ROOT/'templates/sem-violin-pearson/plot_sem_violin_pearson.py').read_bytes(),(CATALOG/card['source']['original_code']).read_bytes())
                    continue
                if card['kind']=='complete_template':
                    current=CATALOG/card['source']['execution_code']
                    self.assertEqual(current.read_bytes(),(CATALOG/card['source']['original_code']).read_bytes())
                    continue
                block=re.search(r'```python\s*\n(.*?)\n```',recipes.extract(card['id']),re.S)
                self.assertIsNotNone(block)
                self.assertEqual(block[1].strip(),(CATALOG/card['source']['original_code']).read_text(encoding='utf8').strip())

    def test_previews_and_compact_index(self):
        index={c['id']:c for c in map(json.loads,(CATALOG/'selection-index.jsonl').read_text(encoding='utf8').splitlines())}
        self.assertEqual(set(index),{c['id'] for c in CARDS})
        for card in CARDS:
            with self.subTest(tid=card['id']):
                self.assertEqual(index[card['id']]['visual_features'],card['visual_features'])
                self.assertEqual(index[card['id']]['composition'],card['composition'])
                for preview in card['previews']:
                    self.assertEqual(hashlib.sha256((CATALOG/preview['path']).read_bytes()).hexdigest(),preview['sha256'])

    def test_omitting_a_key_drawing_operation_produces_a_hint(self):
        # Deliberately remove all calls of one evidenced operation. The rewritten
        # candidate is parsed only; it may depend on omitted artists at runtime.
        for card in CARDS:
            with self.subTest(tid=card['id']):
                source=(CATALOG/card['source']['original_code']).read_text(encoding='utf8')
                spans=[(e['line'],e['end_line']) for p in card['fidelity_checkpoints'] for e in p['evidence']]
                choices=[r for r in review.inspect_source(source) if any(a<=r['line']<=b for a,b in spans)]
                self.assertTrue(choices)
                target=choices[0]['method']
                class Remove(ast.NodeTransformer):
                    def visit_Call(self,node):
                        if review.method(node)==target:return ast.copy_location(ast.Constant(value=None),node)
                        return self.generic_visit(node)
                changed=ast.unparse(Remove().visit(ast.parse(source)))
                report=review.compare_sources(source,changed)
                self.assertTrue(any(f['kind']=='operation_not_found' and f['method']==target for f in report['findings']))


if __name__=='__main__':unittest.main()
