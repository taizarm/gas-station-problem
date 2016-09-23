import unittest
from io import StringIO

from pyramid import testing


# class MockCGIFieldStorage(object):
#     pass

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'gas_station_problem')

    # def test_gas_station_view(self):
    #     from .views import gas_station_view
    #
    #     upload = MockCGIFieldStorage()
    #     upload.file = StringIO('foo')
    #     upload.filename = 'input.csv'
    #
    #     request = testing.DummyRequest(post={'input_file': upload})
    #     info = gas_station_view(request)
    #     self.assertEqual(info['project'], 'gas_station_problem')


class GasStationTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_gas_station_first(self):
        strArr = [4, '1:1', '2:2', '2:2', '3:3']
        from .gasstation import GasStation
        output = GasStation(strArr)

        self.assertEqual(output, 1)

    def test_gas_station_last(self):
        strArr = [5, '0:1', '2:2', '1:2', '1:2', '5:1']
        from .gasstation import GasStation
        output = GasStation(strArr)

        self.assertEqual(output, 5)

    def test_gas_station_impossible(self):
        strArr = [5, '0:1', '1:2', '2:2', '1:2', '2:1']
        from .gasstation import GasStation
        output = GasStation(strArr)

        self.assertEqual(output, 'impossible')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from gas_station_problem import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Gas Station Problem' in res.body)
