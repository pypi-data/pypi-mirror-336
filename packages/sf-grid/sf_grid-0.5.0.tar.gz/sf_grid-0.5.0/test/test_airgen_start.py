import unittest
from grid.repl import GRIDRepl
import subprocess
import time

class TestGRIDReplAirgenSession(unittest.TestCase):

    def setUp(self):
        self.repl = GRIDRepl()
        time.sleep(2)

    def tearDown(self):
        # Ensure all subprocesses are terminated
        self.repl.do_exit(None)
        time.sleep(2)

    def test_airgen_session_start_stop(self):
        # Initialize containers
        self.repl.do_init("airgen @local")

        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        container_names = result.stdout.splitlines()
        self.assertIn("grid_core", container_names)
        self.assertIn("grid_server", container_names)
        self.assertIn("grid_sim_airgen", container_names)

        # Start session
        self.repl.do_session("start test_session ~/.grid/sample_session_config_airgen.json @local")

        # Check if session is running
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        container_names = result.stdout.splitlines()
        self.assertIn("test_session", container_names)

        # Stop session
        self.repl.do_session("stop test_session")

        # Check if session is stopped
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        container_names = result.stdout.splitlines()
        self.assertNotIn("test_session", container_names)

if __name__ == '__main__':
    unittest.main()
