import random
import string
import unittest

from heagVehicleLivedataUtils import vehicleInformation as vehicle_info
from heagVehicleLivedataUtils.vehicleInformation import get_tram_line_color, encode_line_name, get_bus_line_color, \
    tram_default_color, bus_default_color, get_line_color


# ahhh iwi hab ich mitten drin angefangen anders zu importieren


class TestVehicleNumber(unittest.TestCase):

    def test_prefix_on_trams(self):
        #st10
        for i in range(1, 8 + 1):
            self.assertEqual('76', vehicle_info.tram_class_prefix(i))

        # st11
        for i in range(9, 14 + 1):
            self.assertEqual('82', vehicle_info.tram_class_prefix(i))

        # st12
        for i in range(15, 24 + 1):
            self.assertEqual('91', vehicle_info.tram_class_prefix(i))

        # st13
        for i in range(55, 74 + 1):
            self.assertEqual('98', vehicle_info.tram_class_prefix(i))

        # st14
        for i in range(75, 92 + 1):
            self.assertEqual('07', vehicle_info.tram_class_prefix(i))

        # st15
        for i in range(101, 125 + 1):
            self.assertEqual('22', vehicle_info.tram_class_prefix(i))

        # st7
        self.assertEqual('', vehicle_info.tram_class_prefix(31))
        self.assertEqual('', vehicle_info.tram_class_prefix(25))
        self.assertEqual('', vehicle_info.tram_class_prefix(26))

    def test_tram_number(self):
        #st10
        for i in range(1, 8 + 1):
            self.assertEqual(f'76{i}', vehicle_info.get_tram_number(i))

        # st11
        for i in range(9, 14 + 1):
            self.assertEqual(f'82{i}', vehicle_info.get_tram_number(i))

        # st12
        for i in range(15, 24 + 1):
            self.assertEqual(f'91{i}', vehicle_info.get_tram_number(i))

        # st13
        for i in range(55, 74 + 1):
            self.assertEqual(f'98{i}', vehicle_info.get_tram_number(i))

        # st14
        for i in range(75, 92 + 1):
            self.assertEqual(f'07{i}', vehicle_info.get_tram_number(i))

        # st15
        for i in range(101, 125 + 1):
            self.assertEqual(f'22{i}', vehicle_info.get_tram_number(i))

        # st7
        self.assertEqual('31', vehicle_info.get_tram_number(31))
        self.assertEqual('25', vehicle_info.get_tram_number(25))
        self.assertEqual('26', vehicle_info.get_tram_number(26))

    def test_prefix_other_inputs(self):
        # not tram
        # self.assertRaises(vi.tram_class_prefix(0),ERROR??) TODO: wie wollen wir die handlen?
        # self.assertRaises(vi.tram_class_prefix(-10),ERROR??) TODO: wie wollen wir die handlen?
        # self.assertRaises(vi.tram_class_prefix(433),ERROR_BUS?? not a tram) TODO: wie wollen wir die handlen?

        # assert no prefix
        self.assertEqual('', vehicle_info.tram_class_prefix(0))
        self.assertEqual('', vehicle_info.tram_class_prefix(-1))
        self.assertEqual('', vehicle_info.tram_class_prefix(433))


class TestLineName(unittest.TestCase):

    def test_line_encoding(self):
        # tram lines are encoded as themselves
        for tram_line in range(1, 11):
            self.assertEqual(tram_line, vehicle_info.encode_line_name(str(tram_line)))

        # numeric bus lines are also encoded as themselves
        for numeric_bus_line in range(600, 900, 20):
            self.assertEqual(numeric_bus_line, vehicle_info.encode_line_name(str(numeric_bus_line)))

        # check regular bus lines
        for _ in range(100):
            line_id = vehicle_info.encode_line_name(__random_line_name__())
            self.assertTrue(line_id > 0)

        # test improper inputs
        vehicle_info.encode_line_name('')

    def test_line_decoding(self):
        # tram lines are decoded correctly
        for tram_line in range(1, 11):
            self.assertEqual(str(tram_line), vehicle_info.decode_line_id(tram_line))
        # numeric bus lines are also decoded correctly

        for numeric_bus_line in range(600, 900, 20):
            self.assertEqual(str(numeric_bus_line), vehicle_info.decode_line_id(numeric_bus_line))

        # check regular bus lines
        for _ in range(100):
            line_name = __random_line_name__()
            line_name_decoded = vehicle_info.decode_line_id(vehicle_info.encode_line_name(line_name))
            self.assertTrue(line_name, line_name_decoded)

        # test improper inputs
        self.assertEqual('', vehicle_info.decode_line_id(vehicle_info.encode_line_name('')))

        # test decode 0 as no line
        self.assertEqual('No service', vehicle_info.decode_line_id(0))

class TestLineColor(unittest.TestCase):
    def line_color_helper(self, expected_color: str | None, line:str):
        if expected_color is not None:
            self.assertEqual(expected_color, get_tram_line_color(line))
            self.assertEqual(expected_color, get_tram_line_color(encode_line_name(line)))

            self.assertEqual(expected_color, get_bus_line_color(line))
            self.assertEqual(expected_color, get_bus_line_color(encode_line_name(line)))

            self.assertEqual(expected_color, get_line_color(line,'a'))
            self.assertEqual(expected_color, get_line_color(encode_line_name(line),'a'))
        else:
            self.assertEqual(tram_default_color, get_tram_line_color(line))
            self.assertEqual(tram_default_color, get_tram_line_color(encode_line_name(line)))

            self.assertEqual(bus_default_color, get_bus_line_color(line))
            self.assertEqual(bus_default_color, get_bus_line_color(encode_line_name(line)))

            self.assertEqual('a', get_line_color(line, 'a'))
            self.assertEqual('a', get_line_color(encode_line_name(line), 'a'))

    def test_line_color(self):
        self.line_color_helper('#00a650', '2')
        self.line_color_helper('#bf1b2c', 'F')
        self.line_color_helper(None, '721')
        # not checking negative numbers as this is job of line encode/decode

def __random_line_name__(min_length:int =1, max_length:int =10):
    letters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(random.randint(min_length, max_length)))

if __name__ == '__main__':
    unittest.main()
