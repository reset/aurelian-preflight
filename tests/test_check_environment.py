import sys
import unittest
from pathlib import Path

import check_environment


class ParseSemverTest(unittest.TestCase):
    def test_reads_major_minor_patch(self) -> None:
        self.assertEqual(check_environment.parse_semver("3.12.4"), (3, 12, 4))

    def test_fills_missing_parts_with_zero(self) -> None:
        self.assertEqual(check_environment.parse_semver("3.10"), (3, 10, 0))

    def test_ignores_leading_v_and_trailing_words(self) -> None:
        self.assertEqual(check_environment.parse_semver("v2.47.1 (Apple Git-154)"), (2, 47, 1))


class WindowsMountTest(unittest.TestCase):
    def test_path_under_mnt_is_a_windows_mount(self) -> None:
        self.assertTrue(check_environment.running_from_windows_mount(Path("/mnt/c/work")))

    def test_path_under_home_is_not(self) -> None:
        self.assertFalse(check_environment.running_from_windows_mount(Path.home()))


class FindSupportedPythonTest(unittest.TestCase):
    def test_finds_the_running_interpreter_first(self) -> None:
        found = check_environment.find_supported_python()
        self.assertIsNotNone(found)
        assert found is not None
        path, version = found
        self.assertEqual(path, sys.executable)
        self.assertEqual(check_environment.parse_semver(version)[:2], sys.version_info[:2])


if __name__ == "__main__":
    unittest.main()
