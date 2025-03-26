import re
import unittest

import numpy
import pandas as pd

from heagVehicleLivedataUtils.analyze.data import DataAnalysis
from heagVehicleLivedataUtils.analyze.plot import VehicleDataPlotter
from heagVehicleLivedataUtils.vehicleDataUtils.process import get_vehicle_journeys
from heagVehicleLivedataUtils.vehicleInformation import encode_line_name, st15Numbers, articlated_bus_numbers, \
    decode_line_id
from heagVehicleLivedataUtils.vehicleDataUtils.read import verify_vehicledata_format

class TestRead(unittest.TestCase):
    # TODO: what about ill formed data?/ -> error handling
    def test_special_read(self):
        da = DataAnalysis(vehicledata_path="../test/vehicleInfo_test_special_cases/") # TODO seems to have problems with "6E" and such lines
        vehicle_data = da.get_vehicledata()

        timestamp = pd.Timestamp("2024-11-09T09:29:49+0100")

        # bus line as category 1(tram)
        self.assertEqual(vehicle_data.loc[(timestamp, 444),'category'],1)

        # added offset to vehicleid
        self.assertEqual(vehicle_data.loc[(timestamp, 4284), 'lineid'], encode_line_name("L"))

        # line name that can be read as float
        self.assertEqual(vehicle_data.loc[(timestamp, 430), 'lineid'], encode_line_name("4E"))

        # tram vehicleid on bus line
        self.assertEqual(vehicle_data.loc[(timestamp, 112), 'lineid'], encode_line_name("WE2"))


        timestamp = pd.Timestamp("2024-11-09T23:04:49+0100")

        # line name that can be read as float
        self.assertEqual(vehicle_data.loc[(timestamp, 69), 'lineid'], encode_line_name("8E"))

        # switched category
        self.assertEqual(vehicle_data.loc[(timestamp, 114), 'category'], 5)


        timestamp = pd.Timestamp("2024-11-09T23:39:49+0100")

        self.assertEqual(vehicle_data.loc[(timestamp, 405), 'lineid'], encode_line_name("8"))

        self.assertEqual(vehicle_data.loc[(timestamp, 68), 'lineid'], encode_line_name("6E"))

class TestPlot(unittest.TestCase):
    def test_regular_read_and_plot(self):
        da = VehicleDataPlotter(vehicledata_path="../test/vehicleInfo_test/")

        # test if working with data does not throw errors
        da.plot_number_of_trams_in_service(sample_time="15Min",show_plot=False)
        da.plot_all_trams_in_service(sample_time="15Min",show_plot=False)
        da.plot_electric_buses_in_service(sample_time="15Min",show_plot=False)

        da.get_tram_journeys()
        da.get_bus_journeys()

        # check if dataframe is formated to expected spec
        self.assertTrue(verify_vehicledata_format(da.get_vehicledata()))
        #TODO: maybe test out features aswell!


    def test_duplicated_read(self):
        da = VehicleDataPlotter(vehicledata_path="../test/vehicleInfo_test/")
        vehicledata = da.get_vehicledata()
        da = VehicleDataPlotter(pd.concat([vehicledata,vehicledata])) # duplicated dataset

        da.get_trams_in_service()
        da.get_buses_in_service()

        da.get_tram_journeys()
        da.get_bus_journeys()

        da.plot_number_of_trams_in_service(sample_time="15Min", show_plot=False)
        da.plot_all_trams_in_service(sample_time="15Min", show_plot=False)
        da.plot_electric_buses_in_service(sample_time="15Min", show_plot=False)

class TestDataMethods(unittest.TestCase):
    da = DataAnalysis(vehicledata_path="../test/vehicleInfo_journeys/")
    da_big = DataAnalysis(vehicledata_path="../test/vehicleInfo_test/")
    da_empty = DataAnalysis(da.get_vehicledata()[0:0])

    def test_get_journeys_format(self):

        for data_ana in [self.da, self.da_big, self.da_empty]:
            ## tram
            self.assertTrue(
                {'vehicleid', 'lineid', 'start', 'end', 'direction'} <= set(
                    data_ana.get_tram_journeys().columns
                ))
            self.assertTrue(
                {'vehicleid', 'line', 'start', 'end', 'direction'} <= set(
                    data_ana.get_tram_journeys(decode_line_id=True).columns
                ))
            self.assertTrue(
                {'vehicleid', 'lineid', 'start', 'end', 'direction','line_color'} <= set(
                    data_ana.get_tram_journeys(line_colors=True).columns
                ))
            self.assertTrue(
                {'vehicleid', 'line', 'start', 'end', 'direction','line_color'} <= set(
                    data_ana.get_tram_journeys(decode_line_id=True,line_colors=True).columns
                ))

            ## bus
            self.assertTrue(
                {'vehicleid', 'lineid', 'start', 'end', 'direction'} <= set(
                    data_ana.get_bus_journeys().columns
                ))
            self.assertTrue(
                {'vehicleid', 'line', 'start', 'end', 'direction'} <= set(
                    data_ana.get_bus_journeys(decode_line_id=True).columns
                ))
            self.assertTrue(
                {'vehicleid', 'lineid', 'start', 'end', 'direction', 'line_color'} <= set(
                    data_ana.get_bus_journeys(line_colors=True).columns
                ))
            self.assertTrue(
                {'vehicleid', 'line', 'start', 'end', 'direction', 'line_color'} <= set(
                    data_ana.get_bus_journeys(decode_line_id=True, line_colors=True).columns
                ))

        options = ({'decode_line_id':False,"line_colors":False},
                   {'decode_line_id':True,"line_colors":False},
                   {'decode_line_id':False,"line_colors":True},
                   {'decode_line_id':True, "line_colors":True})

        for options in options:
            tram_journeys = self.da.get_tram_journeys(**options)
            self.journeys_format_helper(tram_journeys,**options)

            bus_journeys = self.da.get_tram_journeys(**options)
            self.journeys_format_helper(bus_journeys, **options)

    def journeys_format_helper(self, journeys, decode_line_id=False,line_colors=False):
        self.assertTrue(isinstance(journeys['start'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype))
        self.assertTrue(isinstance(journeys['end'].dtype, pd.core.dtypes.dtypes.DatetimeTZDtype))

        if not decode_line_id:
            self.assertTrue(journeys['lineid'].dtype, numpy.dtypes.Int64DType)

        if line_colors:
            self.assertTrue(journeys['line_color'].map(is_color).prod())

    def test_get_journeys_data(self):
        decoded_lines = self.da_big.get_tram_journeys(decode_line_id=True)['line']
        encoded_lines = self.da_big.get_tram_journeys()['lineid']
        self.assertTrue((decoded_lines== encoded_lines.map(decode_line_id)).prod())

        tram_journeys_color = self.da_big.get_tram_journeys(line_colors=True)['line_color']
        bus_journeys_color = self.da_big.get_bus_journeys(line_colors=True)['line_color']
        self.assertTrue(tram_journeys_color.map(is_color).prod() or tram_journeys_color.empty)
        self.assertTrue(bus_journeys_color.map(is_color).prod() or bus_journeys_color.empty)

        tram_journeys = self.da_big.get_tram_journeys()
        also_tram_journeys = get_vehicle_journeys(self.da_big.get_tram_data())

        self.assertTrue(compare_journeys(tram_journeys,also_tram_journeys))

        bus_journeys = self.da_big.get_bus_journeys()
        also_bus_journeys = get_vehicle_journeys(self.da_big.get_bus_data())

        self.assertTrue(compare_journeys(bus_journeys, also_bus_journeys))

        for vehicles in (st15Numbers, articlated_bus_numbers):
            self.assertTrue(set(self.da_big.get_tram_journeys(vehicles=vehicles)['vehicleid']) <= set(vehicles))
            self.assertTrue(set(self.da_big.get_bus_journeys(vehicles=vehicles)['vehicleid']) <= set(vehicles))

            #TODO: also check if data is the same
            # die tests hier sind iwi noch nicht so meaningful


def is_color(input_string:str):
    return True if re.compile(r"^#[A-Fa-f0-9]{6}$").search(input_string) else False

def compare_journeys(journeys1, journeys2):
    return (journeys1.sort_values(['vehicleid','start']) == journeys2.sort_values(['vehicleid','start'])).min(axis=None)

if __name__ == '__main__':
    unittest.main()
