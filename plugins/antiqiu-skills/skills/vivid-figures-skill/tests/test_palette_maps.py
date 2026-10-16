"""Project palette changes must reach heatmap colors without changing data."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np

SHARED=Path(__file__).resolve().parents[1]/'original/resources/assets/shared-scripts'
sys.path.insert(0,str(SHARED))
import vivid_config as vc
from palette_maps import palette_cmap,palette_stops,contrast_text


class PaletteMapTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.previous=os.environ.get('VIVID_WORKSPACE')
        os.environ['VIVID_WORKSPACE']=str(self.root)

    def tearDown(self):
        if self.previous is None:os.environ.pop('VIVID_WORKSPACE',None)
        else:os.environ['VIVID_WORKSPACE']=self.previous
        self.temp.cleanup()

    def test_switch_all_presets_in_one_process(self):
        samples=[]
        for key in vc.registry()['palettes']:
            vc.write_config(self.root,palette=key)
            colors=palette_cmap('diverging')(np.linspace(0,1,7))
            samples.append(colors)
            self.assertEqual(palette_stops('diverging',count=5)[2],'#ffffff')
        for i,a in enumerate(samples):
            for b in samples[i+1:]:self.assertFalse(np.allclose(a,b))

    def test_custom_colors_and_reversal(self):
        vc.write_config(self.root,palette='custom',colors=['#112233','#cc8844'])
        stops=palette_stops('diverging',center='#eeeeee')
        self.assertEqual(stops,['#112233','#eeeeee','#cc8844'])
        self.assertEqual(palette_stops('diverging',center='#eeeeee',reverse=True),stops[::-1])
        self.assertEqual(palette_stops('sequential')[-1],'#112233')

    def test_text_contrast_accounts_for_alpha(self):
        self.assertEqual(contrast_text('#000000'),'#ffffff')
        self.assertEqual(contrast_text('#000000',alpha=.1),'#333333')
        self.assertEqual(contrast_text('#ffffff'),'#333333')

    def test_helper_default_and_explicit_override(self):
        import plot_utils as pu
        captured=[]
        old_save=pu._save
        old_sns=pu._get_sns
        pu._get_sns=lambda:None
        pu._save=lambda fig,path:captured.append(fig)
        try:
            vc.write_config(self.root,palette='pastel-girl')
            pu.heatmap(np.array([[1.,.4],[.4,1.]]),labels=['A','B'],cmap='viridis')
            self.assertEqual(captured[-1].axes[0].images[0].cmap.name,'viridis')
            pu.heatmap(np.array([[1.,-.4],[-.4,1.]]),labels=['A','B'])
            self.assertTrue(captured[-1].axes[0].images[0].cmap.name.startswith('vivid_'))
        finally:
            pu._save=old_save
            pu._get_sns=old_sns
            import matplotlib.pyplot as plt
            for fig in captured:plt.close(fig)


if __name__=='__main__':unittest.main()
