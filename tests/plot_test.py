import unittest

from src.api.plots import *


class PlotTestCase(unittest.TestCase):

    def test_three_obs(self):
        plot = three_obs(ind=['AG.AGR.TRAC.NO', 'AG.AGR.TRAC.NO', 'AG.AGR.TRAC.NO'], country=['usa', 'afe', 'cpv'])
        self.assertIsNotNone(plot)
        plot.show()

    def test_three_obs_new(self):
        plot = new_multiple_observables_plot([('AG.AGR.TRAC.NO', 'usa'),
                                              ('AG.AGR.TRAC.NO', 'afe'),
                                              ('AG.AGR.TRAC.NO', 'cpv')])
        self.assertIsNotNone(plot)
        plot.show()

    def test_retta_reg(self):
        plot_regression_rect = retta_reg(ind='AG.AGR.TRAC.NO', country='usa')
        self.assertIsNotNone(plot_regression_rect)

    def test_media_mobile(self):
        plot_media_mobile = media_mobile(ind='AG.AGR.TRAC.NO', country='usa', win=3)
        self.assertIsNotNone(plot_media_mobile)
        plot_media_mobile.show()

    def test_media_mobile_new(self):
        plot_media_mobile = media_mobile(ind='AG.AGR.TRAC.NO', country='usa', win=3)
        self.assertIsNotNone(plot_media_mobile)
        plot_media_mobile.show()


if __name__ == '__main__':
    unittest.main()
