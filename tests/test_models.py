import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from monitor.models import USBDevice


class ModelTests(unittest.TestCase):

    def test_fingerprint(self):
        device = USBDevice(
            device_id="USB\\VID_1234&PID_5678\\ABC",
            name="Demo",
            vendor="Vendor",
            vid="1234",
            pid="5678",
            serial="ABC",
            removable=False,
        )

        self.assertEqual(device.fingerprint, device.device_id)

    def test_dict(self):
        device = USBDevice(
            device_id="id",
            name="Demo",
            vendor="Vendor",
            vid="1234",
            pid="5678",
            serial="ABC",
            removable=False,
        )

        self.assertEqual(device.to_dict()["name"], "Demo")


if __name__ == "__main__":
    unittest.main()
