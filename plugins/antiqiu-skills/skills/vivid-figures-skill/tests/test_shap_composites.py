"""Protect alignment, attribution arithmetic and full-composition encodings."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('shap_composites',ROOT/'templates/shap-composites/plot_shap_composites.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class ShapCompositeTests(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def test_csv_alignment_uses_both_ids_and_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            a,b = Path(tmp)/'x.csv',Path(tmp)/'s.csv'
            a.write_text('sample_id,A,B\nx,1,2\ny,3,4\nz,5,6\n')
            b.write_text('sample_id,B,A\nz,60,50\nx,20,10\ny,40,30\n')
            x,s,names=m.load_inputs(a,b)
            np.testing.assert_array_equal(s,x*10)
            b.write_text('sample_id,B,A\nz,60,50\nx,20,10\nx,40,30\n')
            with self.assertRaises(ValueError):m.load_inputs(a,b)

    def test_opposite_signed_effects_do_not_cancel_importance(self):
        s=np.array([[2.,-2.,1.],[-2.,2.,1.],[2.,-2.,1.]])
        names=['A','B','C']; groups={'A':'G1','B':'G1','C':'G2'}
        stats=m.summarize(s,names,groups)
        np.testing.assert_allclose(stats['percent'],[40,40,20])
        self.assertEqual(stats['groups'][0]['percent'],80)
        fig,audit=m.plot_contribution(s,s,names,groups,top=2)
        self.assertEqual(audit['displayed'],['A','B'])
        self.assertEqual(len(audit['ring_features']),3)
        np.testing.assert_allclose([p.get_width() for p in fig.axes[0].patches],[2,2])

    def test_synthetic_shap_adds_to_model_prediction(self):
        with tempfile.TemporaryDirectory() as tmp:
            x,s,names,groups,thresholds=m.demo_data(tmp)
            _,_,model=m.read_table(Path(tmp)/'model.csv')
            np.testing.assert_allclose(model[:,1]+s.sum(axis=1),model[:,0],rtol=1e-12,atol=1e-12)
            self.assertTrue(np.isfinite(s).all())

    def test_no_automatic_threshold_and_scatter_keeps_values(self):
        rng=np.random.default_rng(13); x=rng.normal(size=(25,3)); s=x*[.2,-.5,.1]
        fig,audit=m.plot_dependence(x,s,['A','B','C'],panels=2)
        self.assertEqual(audit['thresholds'],{})
        for collection,j in zip(fig.axes[0].collections,audit['order']):
            np.testing.assert_allclose(collection.get_offsets()[:,0],s[:,j])
        with self.assertRaises(ValueError):
            m.validate_thresholds({'A':{'value':0}},x,['A','B','C'])

    def test_invalid_values_groups_and_constant_features(self):
        x=np.ones((4,3)); s=np.tile([1,2,3],(4,1)); names=['A','B','C']
        np.testing.assert_allclose(m.normalize_feature(x[:,0]),.5)
        self.assertIsNone(m.smooth_trend(x[:,0],s[:,0]))
        for bad in [np.full((4,3),np.nan),np.zeros((4,3)),np.ones((3,3))]:
            with self.assertRaises(ValueError):m.validate_data(x,bad,names)
        with self.assertRaises(ValueError):m.summarize(s,names,{'A':'G1','B':'G2'})


if __name__=='__main__':unittest.main()
