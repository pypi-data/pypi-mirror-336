import unittest
import udalmap


class TestUdalmapBase(unittest.TestCase):

    def setUp(self):
        """Fixture"""
        self.udm = udalmap.UdalMap()
        self.udm_timeout = udalmap.UdalMap(timeout=0.001)
        self.groupid = "E"
        self.subgroupid = "E.1"
        self.indicatorid = "7"
        self.entityid = "01000"
        self.regionid = "20400"
        self.municipalityid = "20005"

    def test_raises_timeout(self):
        """Test timeout raises exception"""
        with self.assertRaises(Exception):
            self.udm_timeout.groups()

    def test_response_groups(self):
        """Test response to groups()"""
        response = self.udm.groups()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)

    def test_response_group(self):
        """Test response to group(groupId)"""
        response = self.udm.group(self.groupid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_subgroups(self):
        """Test response to subgroups()"""
        response = self.udm.subgroups()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)

    def test_response_subgroup(self):
        """Test response to subgroup(subgroupId)"""
        response = self.udm.subgroup(self.subgroupid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicators(self):
        """Test response to indicators()"""
        response = self.udm.indicators()
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)

    def test_response_subgroup_indicators(self):
        """Test response to subgroup_indicators(subgroupId)"""
        response = self.udm.subgroup_indicators(self.subgroupid)
        self.assertIsInstance(response, list)
        self.assertTrue(len(response) > 0)

    def test_response_municipality_indicators_data(self):
        """Test response to municipality_indicators_data(municipalityId)"""
        response = self.udm.municipality_indicators_data(self.municipalityid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicator_data(self):
        """Test response to indicator_data(indicatorId)"""
        response = self.udm.indicator_data(self.indicatorid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicator_entities_data(self):
        """Test response to indicator_entities_data(indicatorId)"""
        response = self.udm.indicator_entities_data(self.indicatorid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicator_entity_data(self):
        """Test response to indicator_entity_data(indicatorId, entityId)"""
        response = self.udm.indicator_entity_data(
            self.indicatorid, self.entityid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicator_regions_data(self):
        """Test response to indicator_regions_data(indicatorId)"""
        response = self.udm.indicator_regions_data(self.indicatorid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicator_region_data(self):
        """Test response to indicator_region_data(indicatorId, regionId)"""
        response = self.udm.indicator_region_data(
            self.indicatorid, self.regionid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicator_municipalities_data(self):
        """Test response to indicator_municipalities_data(indicatorId)"""
        response = self.udm.indicator_municipalities_data(self.indicatorid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def test_response_indicator_municipality_data(self):
        """Test response to indicator_municipality_data(indicatorId, municipalityId)"""
        response = self.udm.indicator_municipality_data(
            self.indicatorid, self.municipalityid)
        self.assertIsInstance(response, dict)
        self.assertTrue(len(response) > 0)

    def tearDown(self):
        """Clean the environment"""
        del self.udm
        del self.udm_timeout
        del self.groupid
        del self.subgroupid
        del self.indicatorid
        del self.entityid
        del self.regionid
        del self.municipalityid


# Make this module executable in unittest
if __name__ == "__main__":
    unittest.main(verbosity=2)
