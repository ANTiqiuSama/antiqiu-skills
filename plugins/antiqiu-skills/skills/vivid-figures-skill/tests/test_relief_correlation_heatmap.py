"""Keep matrix truth, signed relief and colorbar mapping consistent."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('relief_heatmap',ROOT/'catalog/sources/advanced.relief_correlation_heatmap/original.py')
recipe=importlib.util.module_from_spec(spec);spec.loader.exec_module(recipe)


class ReliefCorrelationTests(unittest.TestCase):
    def tearDown(self):plt.close('all')

    def test_correlations_come_from_samples_without_reordering(self):
        samples=np.array([[1.,4.,2.],[2.,3.,5.],[4.,1.,3.],[7.,0.,8.]])
        matrix=recipe.from_samples(samples,['A','B','C'])
        np.testing.assert_allclose(matrix,np.corrcoef(samples,rowvar=False))
        self.assertLess(matrix[0,1],0)
        np.testing.assert_allclose(np.diag(matrix),1.)

    def test_invalid_correlation_and_constant_columns_rejected(self):
        cases=[[[1.,2.],[2.,1.]],[[1.,.3],[.1,1.]],[[.9,0],[0,1]],
               [[1.,.9,.9],[.9,1.,-.9],[.9,-.9,1.]]]
        for matrix in cases:
            with self.subTest(matrix=matrix),self.assertRaises(ValueError):
                recipe.validate_correlation(matrix,[str(i) for i in range(len(matrix))])
        with self.assertRaises(ValueError):recipe.from_samples([[1.,2.],[1.,3.],[1.,4.]],['A','B'])

    def test_signed_height_and_square_face_geometry(self):
        heights=[]
        for r in [-1.,0.,1.]:
            bottom,left,face,height=recipe.cell_geometry(1,2,4,r)
            heights.append(height)
            np.testing.assert_allclose(face[1]-face[0],[1.,0.])
            np.testing.assert_allclose(face[3]-face[0],[0.,1.])
        self.assertLess(heights[0],heights[1]);self.assertLess(heights[1],heights[2])
        np.testing.assert_allclose(heights,[.12,.82,1.52])

    def test_every_cell_preserved_and_faces_match_fixed_colorbar(self):
        matrix=np.array([[1.,-.7],[-.7,1.]])
        cmap=plt.get_cmap('coolwarm')
        fig,stats=recipe.plot_chart(matrix,['A','B'],cmap=cmap)
        self.assertEqual(len(fig.axes[0].patches),12)
        self.assertEqual(len(stats['faces']),4)
        cb=fig.axes[1]._colorbar
        self.assertEqual((cb.norm.vmin,cb.norm.vmax),(-1,1))
        for cell in stats['faces']:
            r=matrix[cell['row'],cell['col']]
            self.assertEqual(cell['r'],r)
            np.testing.assert_allclose(cell['face_color'],cmap(cb.norm(r))[:3])


if __name__=='__main__':unittest.main()
