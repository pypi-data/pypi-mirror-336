import unittest
from grid.repl import GRIDRepl
import subprocess
import time
import json

class TestIsaacSession(unittest.TestCase):

    def setUp(self):
        self.repl = GRIDRepl()
        time.sleep(2)
        self.repl.do_login("@local")

    def tearDown(self):
        # Ensure all subprocesses are terminated
        self.repl.do_exit(None)
        time.sleep(2)

    def test_isaac_session(self):
        # Initialize containers for sim=isaac
        self.repl.do_init("isaac @local")

        # Check if containers are running
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
        container_names = result.stdout.splitlines()
        self.assertIn("grid_core", container_names)
        self.assertIn("grid_server", container_names)
        self.assertIn("grid_sim_isaac", container_names)

        time.sleep(5)

        # Start session using sample isaac session config
        session_id = "test_session"
        self.repl.do_session(f"start {session_id}")

        # Query the is_idle endpoint in grid server
        # Call get_session_info in session_manager.py
        session_info = self.repl.loop.run_until_complete(self.repl.session_manager.get_session_info("localhost", session_id))
        self.assertTrue(session_info.get("has_active_session"))

        # Stop the session
        self.repl.do_session(f"stop {session_id}")

        # Check Docker logs for grid_server to see if session has stopped successfully
        # Query the is_idle endpoint in grid server
        session_info = self.repl.loop.run_until_complete(self.repl.session_manager.get_session_info("localhost", session_id))
        self.assertFalse(session_info.get("has_active_session"))
        
        time.sleep(5)

        self.repl.do_terminate("@local")

if __name__ == '__main__':
    unittest.main()
