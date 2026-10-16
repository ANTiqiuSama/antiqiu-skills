"""The reusable 3D bar must preserve measurements and explicit uncertainty."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'grouped_bar_3d', ROOT/'catalog/sources/advanced.grouped_bar_3d/original.py')
recipe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recipe)


class GroupedBar3DTests(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def test_missing_uncertainty_does_not_invent_error_bars(self):
        values = np.array([[0., 2., 4.], [1., 3., 6.]])
        fig = recipe.plot_chart(values, ['A', 'B'], ['X', 'Y', 'Z'])
        ax = fig.axes[0]
        self.assertEqual(len(ax.lines), 0)
        self.assertEqual([t.get_text() for t in ax.texts],
                         [f'{v:.2f}' for v in values.flat])
        self.assertEqual(len(ax.get_xticks()), 2)
        self.assertEqual(len(ax.get_yticks()), 3)

    def test_asymmetric_error_endpoints_are_not_rescaled(self):
        fig = recipe.plot_chart([[10.]], ['A'], ['X'], errors=[[[2.]], [[3.]]])
        stem = fig.axes[0].lines[0]
        np.testing.assert_allclose(stem.get_data_3d()[2], [8., 13.])
        self.assertGreater(fig.axes[0].get_zlim()[1], 13.)

    def test_invalid_data_and_uncovered_bins_are_rejected(self):
        for values, kwargs in [([[-1.]], {}), ([[float('nan')]], {}),
                               ([[3.]], {'bounds': [0., 1., 2.]}),
                               ([[3.]], {'errors': [[-1.]]})]:
            with self.subTest(values=values, kwargs=kwargs):
                with self.assertRaises(ValueError):
                    recipe.plot_chart(values, ['A'], ['X'], **kwargs)

    def test_custom_palette_changes_colors_without_changing_bins_or_heights(self):
        import vivid_config as vc
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, VIVID_WORKSPACE=directory):
            vc.write_config(directory, palette='custom', colors=['#224466', '#cc8866'])
            fig = recipe.plot_chart([[1., 4.]], ['A'], ['X', 'Y'], bounds=[0., 2., 5.])
            colorbar = fig.axes[1]._colorbar
            self.assertEqual(list(colorbar.boundaries), [0., 2., 5.])
            np.testing.assert_allclose(colorbar.cmap.colors,
                                       [[34/255, 68/255, 102/255], [204/255, 136/255, 102/255]])
            self.assertEqual([t.get_text() for t in fig.axes[0].texts], ['1.00', '4.00'])


if __name__ == '__main__':
    unittest.main()
