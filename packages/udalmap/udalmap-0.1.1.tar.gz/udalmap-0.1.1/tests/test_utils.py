import unittest
import pandas as pd
import matplotlib.pyplot as plt
from udalmap.utils import UdmDf


class TestUdalmapUtils(unittest.TestCase):

    def setUp(self):
        """Fixture"""
        self.udmdf = UdmDf()
        self.indicatorid = "7"
        self.indicatorid_wrong = "777"
        self.body = "entities"
        self.body_wrong = "entitis"
        self.filter_wrong = ["Gipuzku"]
        # Use the Agg backend to avoid GUI output during tests
        plt.switch_backend('Agg')

    def test_response_find(self):
        """Test response to find()"""
        df = self.udmdf.find()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)

    def test_response_get(self):
        """Test response to get(indicatorId, body)"""
        df = self.udmdf.get(self.indicatorid, self.body)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)

    def test_raises_input_error_indicator(self):
        """Test raises exception when invalid indicatorId"""
        with self.assertRaises(Exception):
            self.udmdf.get(self.indicatorid_wrong, self.body)

    def test_raises_input_error_body(self):
        """Test raises exception when invalid body"""
        with self.assertRaises(Exception):
            self.udmdf.get(self.indicatorid, self.body_wrong)

    def test_plot_created(self):
        """Test that a plot was created"""
        num_figures_before = len(plt.get_fignums())
        self.udmdf.plot(self.indicatorid, self.body)
        num_figures_after = len(plt.get_fignums())
        self.assertGreater(num_figures_after, num_figures_before,
                           "The function did not create a plot")

    def test_plot_raises_filter(self):
        """Test that plot wrong filter raises exception"""
        with self.assertRaises(Exception):
            self.udmdf.plot(self.indicatorid, self.body,
                            filters=self.filter_wrong)

    def tearDown(self):
        """Clean the environment"""
        del self.udmdf
        del self.indicatorid
        del self.indicatorid_wrong
        del self.body
        del self.body_wrong
        del self.filter_wrong
        plt.close('all')


# Make this module executable in unittest
if __name__ == "__main__":
    unittest.main(verbosity=2)
