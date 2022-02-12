import unittest

from src.api.plots import *


class PlotTestCase(unittest.TestCase):

    def test_three_obs(self):
        plot = multi_observables_plot([('AG.AGR.TRAC.NO', 'usa'),
                                       ('AG.AGR.TRAC.NO', 'esp'),
                                       ('AG.AGR.TRAC.NO', 'ita')])
        self.assertIsNotNone(plot)
        plot.show()

    def test_retta_reg(self):
        plot_regression_rect = retta_reg(ind='AG.AGR.TRAC.NO', country='usa')
        self.assertIsNotNone(plot_regression_rect)
        plot_regression_rect.show()

    def test_media_mobile(self):
        plot_media_mobile = media_mobile(ind='AG.AGR.TRAC.NO', country='usa', win=3)
        self.assertIsNotNone(plot_media_mobile)
        plot_media_mobile.show()


if __name__ == '__main__':
    unittest.main()
