import unittest
from grid.repl import GRIDRepl
import subprocess
import time

class TestGRIDReplInitTerminate(unittest.TestCase):

    def setUp(self):
        self.repl = GRIDRepl()
        time.sleep(2)
        self.repl.do_login("@local")

    def tearDown(self):
        # Ensure all subprocesses are terminated
        self.repl.do_exit(None)
        time.sleep(2) 

    def test_init_airgen_terminate(self):
        self.repl.do_init("airgen @local")

        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        container_names = result.stdout.splitlines()
        self.assertIn("grid_core", container_names)
        self.assertIn("grid_server", container_names)
        self.assertIn("grid_sim_airgen", container_names)

        self.repl.do_terminate("@local")

        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        container_names = result.stdout.splitlines()
        self.assertNotIn("grid_core", container_names)
        self.assertNotIn("grid_server", container_names)
        self.assertNotIn("grid_sim_airgen", container_names)

if __name__ == '__main__':
    unittest.main()