import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from monitor.comparer import compare_devices
from monitor.models import USBDevice


def device(identifier):
    return USBDevice(
        device_id=identifier,
        name="USB Device",
        vendor="Demo Vendor",
        vid="1234",
        pid="5678",
        serial=identifier,
        removable=False,
    )


class ComparerTests(unittest.TestCase):

    def test_added_removed(self):
        baseline = [device("old")]
        current = [device("new")]

        report = compare_devices(baseline, current)

        self.assertEqual([x.fingerprint for x in report.added], ["new"])
        self.assertEqual([x.fingerprint for x in report.removed], ["old"])
        self.assertTrue(report.changed)

    def test_unchanged(self):
        baseline = [device("same")]
        current = [device("same")]

        report = compare_devices(baseline, current)

        self.assertFalse(report.changed)
        self.assertEqual(report.added, [])
        self.assertEqual(report.removed, [])


if __name__ == "__main__":
    unittest.main()
