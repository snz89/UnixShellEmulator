import unittest
import io
from contextlib import redirect_stdout

from src.emulator import Emulator


class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.emulator = Emulator(
            "testuser", "testcomputer", "example_data/test.tar", "test_log.csv", None)

    def tearDown(self):
        if self.emulator.filesystem:
            self.emulator.filesystem.close()

    def assert_output(self, expected_output, method, *args, **kwargs):
        """Asserts that calling method with the given arguments produces the expected output to stdout."""
        f = io.StringIO()
        with redirect_stdout(f):
            method(*args, **kwargs)

        output = f.getvalue().strip()
        if isinstance(expected_output, list):
            expected_output = "\n".join(expected_output)
        self.assertEqual(output, expected_output)

    # ls tests
    def test_ls_root(self):
        expected_output = [
            ".gitattributes",
            ".gitignore",
            "README.md",
            "java_prac_3/",
            "java_prac_4/",
        ]
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls /")

    def test_ls_relative(self):
        expected_output = ["vehicles/"]
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls java_prac_3")

    def test_ls_invalid_path(self):
        expected_output = "ls: someshittyfile: No such file or directory"
        self.assert_output(
            expected_output, self.emulator.execute_command, "ls someshittyfile")

    # cd tests
    def test_cd_relative(self):
        expected_output = "/java_prac_3"
        self.emulator.execute_command("cd java_prac_3")
        self.assert_output(
            expected_output, self.emulator.execute_command, "pwd")

    def test_cd_invalid_path(self):
        expected_output = "cd: can't cd to someshittyfile: No such file or directory"
        self.assert_output(
            expected_output, self.emulator.execute_command, "cd someshittyfile")

    def test_cd_not_dir(self):
        expected_output = "cd: java_prac_4/app/TestCar.java: Not a directory"
        self.assert_output(
            expected_output, self.emulator.execute_command, "cd java_prac_4/app/TestCar.java")

    # pwd tests
    def test_pwd_initial_directory(self):
        self.assert_output("/", self.emulator.execute_command, "pwd")

    def test_pwd_after_cd(self):
        self.emulator.execute_command("cd java_prac_3")
        self.assert_output(
            "/java_prac_3", self.emulator.execute_command, "pwd")

    def test_pwd_after_cd_and_back(self):
        self.emulator.execute_command("cd java_prac_3")
        self.emulator.execute_command("cd /")
        self.assert_output("/", self.emulator.execute_command, "pwd")

    # history tests
    def test_history_initial(self):
        self.emulator.history.append("history")
        self.assert_output(
            "1 history", self.emulator.execute_command, "history")

    def test_history_cd(self):
        self.emulator.history.append("cd java_prac_3")
        self.emulator.history.append("history")
        self.assert_output(["1 cd java_prac_3", "2 history"],
                           self.emulator.execute_command, "history")

    def test_history_wrong_command(self):
        self.emulator.history.append("hello")
        self.emulator.history.append("history")
        self.assert_output(["1 hello", "2 history"],
                           self.emulator.execute_command, "history")


if __name__ == '__main__':
    unittest.main()
