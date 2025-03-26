import unittest

from heagVehicleLivedataUtils.analyze.data import DataAnalysis
from heagVehicleLivedataUtils.vehicleDataUtils.process import get_vehicle_journeys
from heagVehicleLivedataUtils.vehicleInformation import st15Numbers, articlated_bus_numbers, encode_line_name

import pandas as pd


class testGetJourneys(unittest.TestCase):
    data_test = data = DataAnalysis(vehicledata_path="../test/vehicleInfo_test/").get_vehicledata().reset_index()
    data_test_journeys = DataAnalysis(vehicledata_path="../test/vehicleInfo_journeys/").get_vehicledata().reset_index()

    def test_getJourneys_format(self):
        journeys = get_vehicle_journeys(self.data_test)

        self.assertTrue({'vehicleid', 'lineid', 'start', 'end', 'direction'} <= set(journeys.columns))

        self.assertTrue(isinstance(journeys['start'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype))
        self.assertTrue(isinstance(journeys['end'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype))

        self.assertEqual((journeys['start'] <= journeys['end']).prod(), 1)

        self.assertEqual((journeys['lineid'] == 0).sum(), 0)

    def test_journeys_data(self):
        journeys = get_vehicle_journeys(self.data_test_journeys)

        bus1_journeys = journeys[journeys['vehicleid'] == 375].to_dict(orient='records')
        self.assertEqual(len(bus1_journeys), 1)
        self.check_journey_data(bus1_journeys[0],
                                start="2024-11-08 23:54:48+01:00",
                                end="2024-11-09 00:10:00+01:00",
                                vehicleid=375,
                                lineid="WE2",
                                direction="Worfelden Siedlung Hesselrod")

        bus2_journeys = journeys[journeys['vehicleid'] == 333].to_dict(orient='records')
        self.assertEqual(len(bus2_journeys), 1)
        self.check_journey_data(bus2_journeys[0],
                                start="2024-11-09 00:10:00+01:00",
                                end="2024-11-09 00:10:00+01:00",
                                vehicleid=333,
                                lineid="TEST",
                                direction="Hesselrod")

        tram1_journeys = journeys[journeys['vehicleid'] == 15].to_dict(orient='records')
        self.assertEqual(len(tram1_journeys), 3)
        self.check_journey_data(tram1_journeys[0],
                                start="2024-11-08 23:54:48+01:00",
                                end="2024-11-08 23:57:48+01:00",
                                vehicleid=15,
                                lineid="8",
                                direction="Arheilgen Dreieichweg")

        self.check_journey_data(tram1_journeys[1],
                                start="2024-11-08 23:59:48+01:00",
                                end="2024-11-09 00:05:00+01:00",
                                vehicleid=15,
                                lineid="7",
                                direction="Arheilgen Dreieichweg")

        self.check_journey_data(tram1_journeys[2],
                                start="2024-11-09 00:10:00+01:00",
                                end="2024-11-09 00:10:00+01:00",
                                vehicleid=15,
                                lineid="8",
                                direction="TestTestTest")

        tram2_journeys = journeys[journeys['vehicleid'] == 105].to_dict(orient='records')
        self.assertEqual(len(tram2_journeys), 2)
        self.check_journey_data(tram2_journeys[0],
                                start="2024-11-08 23:54:48+01:00",
                                end="2024-11-08 23:59:48+01:00",
                                vehicleid=105,
                                lineid="8",
                                direction="Arheilgen Dreieichweg")

        self.check_journey_data(tram2_journeys[1],
                                start="2024-11-09 00:05:00+01:00",
                                end="2024-11-09 00:05:00+01:00",
                                vehicleid=105,
                                lineid="8",
                                direction="TestTestTest")

    def check_journey_data(self, journey, *, start: str, end: str, vehicleid, lineid, direction):
        self.assertEqual(pd.Timestamp(start), journey['start'])
        self.assertEqual(pd.Timestamp(end), journey['end'])
        self.assertEqual(vehicleid, journey['vehicleid'])
        self.assertEqual(encode_line_name(lineid), journey['lineid'])
        self.assertEqual(direction, journey['direction'])

if __name__ == '__main__':
    unittest.main()
