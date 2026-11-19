import os
import tempfile
import unittest

import tracker


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.db = os.path.join(tempfile.mkdtemp(), "test.json")

    def test_add_and_list(self):
        tracker.add_bug("Login fails", "high", self.db)
        tracker.add_bug("Typo in footer", "low", self.db)
        bugs = tracker.list_bugs(db=self.db)
        self.assertEqual(len(bugs), 2)
        self.assertEqual(bugs[0]["title"], "Login fails")  # high first

    def test_status_change(self):
        b = tracker.add_bug("Crash on start", db=self.db)
        tracker.set_status(b["id"], "closed", self.db)
        self.assertEqual(len(tracker.list_bugs("closed", self.db)), 1)

    def test_invalid_severity(self):
        with self.assertRaises(ValueError):
            tracker.add_bug("x", "urgent", self.db)

    def test_missing_bug(self):
        with self.assertRaises(KeyError):
            tracker.set_status(99, "closed", self.db)


if __name__ == "__main__":
    unittest.main()
