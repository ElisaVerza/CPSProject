import unittest

from opandas_wb.api.plots import *


class PlotTestCase(unittest.TestCase):

    def test_three_obs(self):
        # provo a graficare lo stesso indicatore di 3 nazioni diverse
        plot = multi_indicator_plot([('AG.AGR.TRAC.NO', 'usa'),
                                     ('AG.AGR.TRAC.NO', 'esp'),
                                     ('AG.AGR.TRAC.NO', 'ita')])
        self.assertIsNotNone(plot)
        plot.show()

    def test_retta_reg(self):
        # provo a graficare la retta di regressione e i punti osservabili di un indicatore
        plot_regression_rect = retta_reg(ind='AG.AGR.TRAC.NO', country='usa')
        self.assertIsNotNone(plot_regression_rect)
        plot_regression_rect.show()

    def test_media_mobile(self):
        # provo a graficare la media mobile per gli osservabili di un indicatore
        plot_media_mobile = media_mobile(ind='SP.RUR.TOTL.ZS', country='usa', win=3)
        self.assertIsNotNone(plot_media_mobile)
        plot_media_mobile.show()

    def test_differenze_prime(self):
        # provo a graficare le differenze prime per gli osservabili di un indicatore
        plot_differenze_prime = diff_prime(ind='AG.AGR.TRAC.NO', country='usa')
        self.assertIsNotNone(plot_differenze_prime)
        plot_differenze_prime.show()

    def test_differenze_prime_percentuali(self):
        # provo a graficare le differenze prime precentuali per gli osservabili di un indicatore
        plot_differenze_prime_perc = diff_prime_perc(ind='AG.AGR.TRAC.NO', country='usa')
        self.assertIsNotNone(plot_differenze_prime_perc)
        plot_differenze_prime_perc.show()

    def test_covarianza(self):
        # calcolo la covarianza tra gli osservabili di due diversi indicatori dello stesso topic (stessa nazione)
        tup = [('SP.RUR.TOTL', 'usa'), ('AG.AGR.TRAC.NO', 'usa')]
        cov = covarianza(tup[0], tup[1])
        self.assertEqual(cov, -724290658071.9613)
        print("\nCov({},{}) = {}".format(tup[0][0], tup[1][0], cov))

        tup2 = [('AG.AGR.TRAC.NO', 'usa'), ('AG.AGR.TRAC.NO', 'usa')]
        cov = covarianza(tup2[0], tup2[1])
        self.assertTrue(cov > 0)
        print("\nCov({},{}) = {}".format(tup2[0][0], tup2[1][0], cov))

        # mostro il grafico che compara i valori per anno delle due serie di osservabili,
        # per verificare che la correlazione tra le due serie e che abbia senso con la covarianza
        # cov/corr > 0 al crescere dei valori di una serie, cresce anche l'altra(retta di regressione con coeff ang>0)
        # cov/corr < 0 al crescere dei valori di una serie, l'altra decresce e viceversa (retta di regressione con m<0)
        # cov/corr = 0 -> scorrelate. Si vedono tutti i punti sparsi.
        cmp_scatter_plot(tup[0], tup[1]).show()  # corr = -0.7, covarianza negativa

        # poiché era lo stesso dataset, in questo caso tutti i punti sono allineati da una retta con m = 1
        cmp_scatter_plot(tup2[0], tup2[1]).show()  # corr = 1, covarianza positiva = varianza


if __name__ == '__main__':
    unittest.main()
