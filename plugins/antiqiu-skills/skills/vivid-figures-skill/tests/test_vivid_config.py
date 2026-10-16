"""Behavioral checks for portable configuration, palette order and bootstrap."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / 'original/resources/assets/shared-scripts'
sys.path.insert(0, str(SHARED))
import vivid_config as vc


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='vivid-config-test-')
        self.root = Path(self.temp.name)
        self.previous = Path.cwd()
        self.old_env = os.environ.pop('VIVID_WORKSPACE', None)
        os.chdir(self.root)

    def tearDown(self):
        os.chdir(self.previous)
        if self.old_env is not None:
            os.environ['VIVID_WORKSPACE'] = self.old_env
        self.temp.cleanup()

    def test_default_without_instruction_file(self):
        self.assertEqual(vc.load_config()['palette'], 'olive-apricot')
        self.assertEqual(vc.palette_colors(), vc.registry()['palettes']['olive-apricot']['colors'])

    def test_all_palettes_from_nested_directory(self):
        nested = self.root / 'figures/a/b/c'
        nested.mkdir(parents=True)
        for name, item in vc.registry()['palettes'].items():
            vc.write_config(self.root, palette=name)
            os.chdir(nested)
            self.assertEqual(vc.palette_colors(), item['colors'])
        self.assertFalse((self.root / 'CLAUDE.md').exists())

    def test_custom_order_and_other_settings_preserved(self):
        colors = ['#ABCDEF', '#123456', '#BC986A']
        vc.write_config(self.root, palette='custom', colors=colors, title='existing', style='clean_open')
        self.assertEqual(vc.palette_colors(), colors)
        self.assertEqual(vc.categorical_colors(), colors)
        vc.write_config(self.root, palette='blue-pink')
        config = vc.load_config()
        self.assertEqual(config['title'], 'existing')
        self.assertNotIn('colors', config)

    def test_invalid_colors_do_not_overwrite_config(self):
        vc.write_config(self.root, palette='olive-apricot')
        before = (self.root / '.vivid/config.json').read_bytes()
        with self.assertRaises(ValueError):
            vc.write_config(self.root, palette='custom', colors=['bad'])
        self.assertEqual(before, (self.root / '.vivid/config.json').read_bytes())

    def test_setup_style_uses_project_configuration(self):
        import plot_utils as pu
        import matplotlib
        for name, item in vc.registry()['palettes'].items():
            vc.write_config(self.root, palette=name)
            pu.setup_style()
            expected = vc.categorical_colors()
            self.assertEqual(pu.PALETTE, expected)
            self.assertEqual(pu.COLORS['primary'], expected[0])
            self.assertEqual(matplotlib.rcParams['axes.prop_cycle'].by_key()['color'], expected)
            self.assertFalse(matplotlib.rcParams['axes.spines.top'])

    def test_fixed_category_order_keeps_original_scale_and_explicit_lists(self):
        import plot_utils as pu
        for name, item in vc.registry()['palettes'].items():
            vc.write_config(self.root, palette=name)
            raw = list(item['colors'])
            pu.setup_style(name)
            self.assertEqual(pu.PALETTE, vc.categorical_colors())
            self.assertCountEqual(pu.PALETTE, raw)
            self.assertEqual(vc.palette_colors(), raw)
        pu.setup_style(['#123456', '#ABCDEF'])
        self.assertEqual(pu.PALETTE, ['#123456', '#ABCDEF'])

    def test_bootstrap_writes_neutral_files_and_preserves_user_edits(self):
        (self.root / '_utils').mkdir()
        custom = self.root / '_utils/plot_utils.py'
        custom.write_text('# user customization\n', encoding='utf-8')
        subprocess.run([sys.executable, str(ROOT / 'original/resources/scripts/bootstrap.py'),
                        '--workspace', str(self.root)], check=True, capture_output=True)
        self.assertEqual(custom.read_text(), '# user customization\n')
        self.assertTrue((self.root / '.vivid/config.json').is_file())
        self.assertTrue((self.root / '.vivid/runtime.json').is_file())
        self.assertTrue((self.root / '_utils/palettes.json').is_file())
        self.assertEqual(list(self.root.rglob('*.enc')), [])

    def test_bootstrap_nested_project_does_not_update_parent(self):
        vc.write_config(self.root, palette='blue-pink', title='parent project')
        before = (self.root / '.vivid/config.json').read_bytes()
        child = self.root / 'new project'
        child.mkdir()
        subprocess.run([sys.executable, str(ROOT / 'original/resources/scripts/bootstrap.py'),
                        '--workspace', str(child)], check=True, capture_output=True)
        self.assertEqual((self.root / '.vivid/config.json').read_bytes(), before)
        self.assertTrue((child / '.vivid/runtime.json').is_file())
        self.assertEqual(vc.load_config(child)['palette'], 'olive-apricot')
        self.assertNotIn('title', vc.load_config(child))


if __name__ == '__main__':
    unittest.main()
