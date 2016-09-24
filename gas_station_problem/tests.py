import unittest

from pyramid import testing
from .gasstation import GasStationClass


class GasStationTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.obj = GasStationClass()

    def tearDown(self):
        testing.tearDown()

    def test_returnFistNode(self):
        self.assertEqual(self.obj.GasStation([2, '2:2', '4:3']), '1')
        self.assertEqual(self.obj.GasStation([4, '1:1', '2:2', '2:2', '3:3']), '1')

    def test_returnLastNode(self):
        self.assertEqual(self.obj.GasStation([2, '2:3', '4:3']), '2')
        self.assertEqual(self.obj.GasStation([5, '0:1', '2:2', '1:2', '1:2', '5:1']), '5')

    def test_returnNodeInTheMiddle(self):
        self.assertEqual(self.obj.GasStation([5, '0:1', '1:2', '5:1', '1:2', '0:1']), '3')

    def test_returnImpossible(self):
        self.assertEqual(self.obj.GasStation([3, '3:5', '3:5', '3:5']), 'impossible')
        self.assertEqual(self.obj.GasStation([3, '3:2', '3:5', '3:5']), 'impossible')
        self.assertEqual(self.obj.GasStation([4, '3:2', '3:3', '3:7', '1:7']), 'impossible')

    def test_LengthLessThan2_returnInvalidInput(self):
        self.assertEqual(self.obj.GasStation(), 'invalid input')
        self.assertEqual(self.obj.GasStation([0]), 'invalid input')
        self.assertEqual(self.obj.GasStation([1, '0:1']), 'invalid input')

    def test_InvalidNodeFormat_returnInvalidInput(self):
        self.assertEqual(self.obj.GasStation(['kk', '01:4', '03:3']), 'invalid input')
        self.assertEqual(self.obj.GasStation([2, ':1', '2:3']), 'invalid input')
        self.assertEqual(self.obj.GasStation([2, '1', '2:3']), 'invalid input')
        self.assertEqual(self.obj.GasStation([2, '1:', '2:3']), 'invalid input')
        self.assertEqual(self.obj.GasStation([2, '1:h', '2:3']), 'invalid input')
        self.assertEqual(self.obj.GasStation([2, '1:4', 'k:3']), 'invalid input')

    def test_InvalidLengthInfo_returnInvalidInput(self):
        self.assertEqual(self.obj.GasStation([3, '1:1', '2:2', '0:3', '8:9']), 'invalid input')
        self.assertEqual(self.obj.GasStation([5, '1:1', '2:2', '0:3']), 'invalid input')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from gas_station_problem import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        res = self.testapp.get('/', status=200)
        self.assertTrue(b'Gas Station Problem' in res.body)
