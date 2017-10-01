import unittest
from iteration_3.src.device import *


class DeviceTestCase(unittest.TestCase):
    def setUp(self):
        self.device = Device(123)

    def test_return_on(self):
        self.assertEqual(self.device.return_one(),1)
