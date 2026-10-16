"""Protect count units and per-group transforms in the multi-axis histogram."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('multi_y_hist',ROOT/'catalog/sources/advanced.multi_y_gradient_hist/original.py')
recipe=importlib.util.module_from_spec(spec);spec.loader.exec_module(recipe)


class MultiYHistogramTests(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def test_counts_and_normal_curve_frequency_scale(self):
        groups={'A':np.array([-2.,-1.,0.,1.,2.]),'B':np.array([-4.,-1.,2.,5.])}
        fig,stats=recipe.plot_chart(groups,bins=np.arange(-5.,8.,2.))
        for i,(name,values) in enumerate(groups.items()):
            self.assertEqual(sum(stats[i]['counts']),len(values))
            self.assertAlmostEqual(stats[i]['mean'],values.mean())
            line=fig.axes[0].lines[i]
            self.assertEqual(line.get_transform(),fig.axes[i].transData)
            x,y=line.get_data()
            expected=len(values)*2/(values.std()*np.sqrt(2*np.pi))*np.exp(-.5*((x-values.mean())/values.std())**2)
            np.testing.assert_allclose(y,expected)

    def test_no_fit_allows_constant_data_without_fabricating_spread(self):
        fig,stats=recipe.plot_chart({'A':[3.,3.,3.]},fit=False)
        self.assertEqual(len(fig.axes[0].lines),0)
        self.assertEqual(stats[0]['std_mle'],0.)
        self.assertEqual(sum(stats[0]['counts']),3)

    def test_bad_samples_bins_and_clipping_rejected(self):
        cases=[({'A':[1.,float('nan')]},{}),({'A':[1.,1.]},{}),
               ({'A':[0.,1.,2.]},{'bins':[0.,1.,3.]}),
               ({'A':[0.,1.,2.]},{'bins':[0.,.5,1.]}),
               ({'A':[0.,1.,2.]},{'ylimits':[(0,.1)]})]
        for groups,kwargs in cases:
            with self.subTest(groups=groups,kwargs=kwargs),self.assertRaises(ValueError):
                recipe.plot_chart(groups,**kwargs)

    def test_three_visible_colored_axes_and_transparent_gradients(self):
        fig,stats=recipe.plot_chart({'A':[-2.,0.,2.],'B':[-5.,0.,5.],'C':[-1.,0.,1.]})
        self.assertEqual(len(fig.axes),3)
        for i,ax in enumerate(fig.axes):
            self.assertTrue(ax.spines['left' if i==0 else 'right'].get_visible())
            alpha=fig.axes[0].collections[i].get_facecolors()[:,3]
            self.assertLess(alpha.min(),.05)
            self.assertGreater(alpha.max(),.7)
            self.assertLess(alpha.max(),1.)
        self.assertEqual(fig.axes[0].get_ylabel(),'Frequency')
        self.assertEqual(fig.axes[2].spines['right'].get_position(),('axes',1.12))

    def test_group_specific_bins_scale_each_fit_by_its_own_bin_width(self):
        groups={'A':[-3.,-1.,1.,3.],'B':[-4.,-2.,2.,4.]}
        bins={'A':np.arange(-4.,5.,2.),'B':np.arange(-6.,7.,3.)}
        fig,stats=recipe.plot_chart(groups,bins=bins)
        for i,(name,values) in enumerate(groups.items()):
            self.assertEqual(sum(stats[i]['counts']),len(values))
            np.testing.assert_allclose(stats[i]['bin_edges'],bins[name])
            x,y=fig.axes[0].lines[i].get_data()
            width=np.diff(bins[name])[0]
            sigma=np.std(values)
            expected=len(values)*width/(sigma*np.sqrt(2*np.pi))*np.exp(-.5*((x-np.mean(values))/sigma)**2)
            np.testing.assert_allclose(y,expected)


if __name__=='__main__':unittest.main()
