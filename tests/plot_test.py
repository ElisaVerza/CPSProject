import unittest

from src.api.plots import three_obs, retta_reg, media_mobile


class PlotTestCase(unittest.TestCase):

    def test_three_obs(self):
        # Todo: non è un plot
        plot = three_obs(ind=['AG.AGR.TRAC.NO', 'AG.AGR.TRAC.NO', 'AG.AGR.TRAC.NO'], country=['usa', 'afe', 'cpv'])
        self.assertIsNotNone(plot)

    def test_retta_reg(self):
        plot_regression_rect = retta_reg(ind='AG.AGR.TRAC.NO', country='usa')
        self.assertIsNotNone(plot_regression_rect)

    def test_media_mobile(self):
        plot_media_mobile = media_mobile(ind='AG.AGR.TRAC.NO', country='usa', win=3)
        self.assertIsNotNone(plot_media_mobile)


if __name__ == '__main__':
    unittest.main()
