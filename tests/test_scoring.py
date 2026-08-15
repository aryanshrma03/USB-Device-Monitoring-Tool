import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from monitor.models import USBDevice
from monitor.scoring import device_risk, report_score


def device(vendor="Vendor", serial="SERIAL", removable=False):
    return USBDevice(
        device_id="id",
        name="USB Device",
        vendor=vendor,
        vid="1234",
        pid="5678",
        serial=serial,
        removable=removable,
    )


class ScoringTests(unittest.TestCase):

    def test_new_device(self):
        self.assertEqual(device_risk(device()), 20)

    def test_removable_unknown(self):
        value = device_risk(device(vendor="Unknown", serial="", removable=True))
        self.assertEqual(value, 60)

    def test_report(self):
        score, severity = report_score(
            [device(removable=True)],
            [],
        )

        self.assertEqual(score, 45)
        self.assertEqual(severity, "MEDIUM")


if __name__ == "__main__":
    unittest.main()
