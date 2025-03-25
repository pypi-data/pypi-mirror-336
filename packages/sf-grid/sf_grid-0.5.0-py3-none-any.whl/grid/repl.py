import asyncio
import os
import webbrowser
import json
import logging
from cmd import Cmd
from art import tprint
from tabulate import tabulate
from grid.sdk.session_manager import GRIDSessionManager
from grid.sdk.resource_manager import GRIDResourceManager
from grid.sdk.commander.client import CommanderClient
from grid.sdk.commander.server import CommanderServer

from grid.utils.config_handler import ConfigHandler
from grid.utils.airgen_utils import AirGenUtils
from grid.utils.isaac_utils import IsaacUtils
from grid.utils.grid_asset_downloader import GRIDAssetDownloader
import requests
from packaging import version
from importlib.metadata import version as current_version
import subprocess
import platform

class GRIDRepl(Cmd):
    prompt = 'GRID \033[91m#\033[0m '
    intro = tprint("\nGRID", "colossal")

    def __init__(self):
        super().__init__()
        self._setup_logging()
        self._print_intro()
        self.check_for_updates()
        self._initialize_managers()
        self._initialize_commander()
        self._initialize_assets()
        self.sim_options = {1: "airgen", 2: "isaac"}
        self.sim_utils_mapping = {
            "airgen": AirGenUtils,
            "isaac": IsaacUtils
        }
        self.sim_name = None
        print("Type 'help' or 'license' for more info.\n")

    def check_for_updates(self):
        """Check if there is a more recent version of the GRID SDK available on PyPI."""
        
        current_grid_version = current_version("sf-grid")

        try:
            response = requests.get(f"https://pypi.org/pypi/sf-grid/json")
            latest_version = response.json()["info"]["version"]

            if version.parse(latest_version) > version.parse(current_grid_version):
                print(f"\033[93mA new version of GRID SDK is available: {latest_version} (current: {current_grid_version})\033[0m")
                print("\033[93mYou can update using: pip install --upgrade grid-sdk\033[0m")
        except requests.RequestException as e:
            self.logger.error(f"An error occurred while checking for updates: {e}", exc_info=True)

    def _print_intro(self):
        print("General Robot Intelligence Development Platform - Enterprise version \nDeveloped by Scaled Foundations, Inc. (c) 2025\n")

    def _initialize_managers(self):
        token_data, resource_data = ConfigHandler.load_resource_config()
        self.resource_manager = GRIDResourceManager(resource_data)
        self.session_manager = GRIDSessionManager(token_data)
        self.token_data = token_data

    def _initialize_commander(self):
        self.commander = CommanderClient()
        self.loop = asyncio.get_event_loop()

        if self.resource_manager.host_grid_local:
            self.commander_server = CommanderServer()
            self.commander_server.start()
        else:
            self.commander_server = None

    def _initialize_assets(self):
        os.makedirs(os.path.expanduser("~/.grid/airgenbins"), exist_ok=True)
        os.makedirs(os.path.expanduser("~/.grid/isaac"), exist_ok=True)
        GRIDAssetDownloader.download_sample_notebooks()
        GRIDAssetDownloader.download_model_weights(self.token_data["storage_token"])

    def _run_commander_server(self):
        try:
            self.commander_server.run()
        except Exception as e:
            self.logger.error(f"An error occurred while running the CommanderServer: {e}", exc_info=True)

    def _setup_logging(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        file_handler = logging.FileHandler('grid_repl.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def cmdloop(self, intro=None):
        while True:
            try:
                super().cmdloop(intro)
                break
            except Exception as e:
                self.logger.error(f"An error occurred: {str(e)}", exc_info=False)
                intro = ''

    def handle_node_command(self, arg, default_node='local'):
        args = arg.split()
        if len(args) > 1:
            print(f"Invalid command. Use '{args[0]}' or '{args[0]} @nodename'.")
            return None
        return arg[1:] if arg.startswith('@') else default_node

    def do_exit(self, _):
        """Exit the console."""
        if self.session_manager.session_nodes:
            if os.isatty(0):
                print("\033[93mWarning: There are active sessions running. Are you sure you want to exit?\033[0m")
                response = input("Enter 'Y' to exit or 'N' to cancel: ")
                if response.lower() == 'y':
                    print("Exiting GRID Console...")
                else:
                    print("Exit cancelled.")
                    return False
            else:
                print("\033[93mWarning: There are active sessions running. Exiting without confirmation due to non-interactive mode.\033[0m")
        
        if self.commander_server:
            self.commander_server.stop()
        return True

    def do_EOF(self, _):
        """Exit the console on EOF (Ctrl+D)"""
        print("\nExiting GRID Console...")

        if self.commander_server:
            self.commander_server.stop()
        return True
    
    def do_license(self, _):
        """Display the license terms."""
        print("Opening license page in the browser...")
        webbrowser.open("https://scaledfoundations.ai/enterprise-license")

    def do_login(self, arg):
        """Login to the GRID registry using username and password/access token

        login @nodename : Login through the specified node (local by default)"""
        node_name = self.handle_node_command(arg)
        username = self.token_data["username"]
        password = self.token_data["password"]
        self.commander.login_registry(node_name, username, password)

    def select_sim(self):
        while True:
            print("Please choose the simulator you wish to use:")
            for key, value in self.sim_options.items():
                print(f"{key}: {value}")
            try:
                choice = int(input("Enter your choice: "))
                if choice in self.sim_options:
                    return self.sim_options[choice]
                print("Invalid choice, try again.")
            except ValueError:
                print("Please enter a valid number.")

    def do_init(self, arg):
        """Spin up the GRID containers.

        init simname @nodename : Start the containers on specified node (local by default)"""

        args = arg.split()
        if len(args) > 2:
            print("Invalid init command. Syntax should be 'init sim_name @node_name'")
            return

        node_name = self.handle_node_command(args[-1]) if args and args[-1].startswith('@') else "local"
        sim_name = args[0] if args else self.select_sim()
        if sim_name not in self.sim_options.values():
            print("You have specified a simulator that is either unavailable or invalid.")
            sim_name = self.select_sim()

        self.sim_name = sim_name
        self.commander.set_sim(node_name, sim_name)

        if self.commander.check_grid_containers(node_name):
            print(f"\033[92mAll containers are already up and running on {node_name}.\033[0m")
            return
        else:
            print(f"Starting GRID containers for {sim_name} on {node_name}...")
            self.commander.init_containers(node_name)
        
        print("Setting up assets...", end=' ')
        if not self.sim_utils_mapping[self.sim_name].post_init(self.token_data["storage_token"]):
            self.logger.error(f"Failed to download assets for {sim_name}.")
            return

        print("Done.")

    def do_terminate(self, arg):
        """Terminate the GRID containers.

        terminate @nodename : Stop the containers on specified node (local by default)"""
        node_name = self.handle_node_command(arg)
        self.commander.kill_containers(node_name)

    def do_update(self, arg):
        """Update the GRID containers.

        update @nodename : Update the containers on specified node (local by default)"""
        args = arg.split()
        node_name = self.handle_node_command(args[-1]) if args and args[-1].startswith('@') else "local"
                
        if not self.sim_name:
            sim_name = args[0] if args else self.select_sim()
            if sim_name not in self.sim_options.values():
                print("You have specified a simulator that is either unavailable or invalid.")
                sim_name = self.select_sim()
                
            self.commander.set_sim(node_name, sim_name)
            self.sim_name = sim_name
                
        print(f"Checking for container updates...")
        self.commander.update_containers(node_name)
        
        print("Updating assets...")
        self.sim_utils_mapping[self.sim_name].post_init(self.token_data["storage_token"], force_redownload=True)
        print("Done.")

    def do_clear(self, _):
        """Clear the terminal output."""
        os.system("clear")

    def do_node(self, arg):
        """Manage nodes:

        node list : List all nodes with their IP addresses"""
        args = arg.split()
        if len(args) < 1:
            print("Invalid node command. Use 'node list'.")
            return

        if args[0] == 'list':
            node_list = self.resource_manager.list_nodes()
            if node_list:
                print(tabulate(node_list, headers="keys", tablefmt="grid"))
            else:
                print("No nodes found in the configuration.")
        else:
            print("Invalid node command.")

    def do_session(self, arg):
        """Manage sessions:

        session start <session_id> <config_path> @<nodename>  : Start a session (uses a sample config if none provided)
        session stop <session_id> : Stop the specified session
        session list : List currently active sessions"""
        if self.session_manager is None:
            print("Session manager not initialized. Use 'connect' command first.")
            return

        args = arg.split()
        if len(args) < 1:
            print("Invalid session command. Use 'session start', 'session stop', or 'session list'.")
            return

        node_name = self.handle_node_command(args[-1]) if args and args[-1].startswith('@') else "local"
        node_ip = self.resource_manager.get_ip_for_resource(node_name)
        command = args[0]
        
        if command == 'start' and len(args) >= 2:      
            if not self.commander.check_grid_containers(node_name):
                print("\033[93mOne or more GRID containers are not up. Please run `init` before attempting to run session commands.\033[0m")
                return

            session_config_path = args[2] if len(args) > 2 else self._get_sample_config_path()
            self.loop.run_until_complete(self._start_session(args[1], session_config_path, node_ip))
        elif command == 'stop' and len(args) == 2:
            self.loop.run_until_complete(self._stop_session(args[1]))
        elif command == 'list':
            self.loop.run_until_complete(self._list_sessions())
        else:
            print("Invalid session command.")

    def _get_sample_config_path(self):
        sim_util_class = self.sim_utils_mapping[self.sim_name]
        sample_config = sim_util_class.create_sample_config()
        session_config_path = f"~/.grid/sample_session_config_{self.sim_name}.json"
        print(f"No session configuration was passed. Using a sample configuration from {session_config_path}...")

        config_path = os.path.abspath(os.path.expanduser(session_config_path))
        with open(config_path, 'w') as output_file:
            json.dump(sample_config, output_file, indent=4)
        return session_config_path

    def do_open(self, arg):
        """Open an entity (notebook, simulation, or telemetry).
        
        Open notebook: open nb @nodename (e.g. @local)
        Open simulation streaming: open sim @nodename
        Open telemetry visualization: open viz @nodename
        """
        args = arg.split()
        if len(args) < 2:
            print("Invalid open command. Use 'open nb | sim | viz | code @node_name'.")
            return
        self._open_entity(args[0], args[1])

    async def _start_session(self, session_id: str, config_path: str, node_ip: str):
        await self.session_manager.start_session(session_id, config_path, node_ip)

    async def _stop_session(self, session_or_node_id: str):
        if session_or_node_id.startswith('@'):
            node_id = session_or_node_id[1:]
            node_ip = self.resource_manager.get_ip_for_resource(node_id)
            
            session_id = await self.session_manager.get_session_id_by_node(node_ip)
            
            if not session_id:
                print("No active sessions found to terminate.")
                return False
            
            print(f"Stopping all sessions on node {node_id} ...")
        else:
            session_id = session_or_node_id
            node_ip = self.session_manager.session_nodes.get(session_id)
            
        print(f"Stopping session {session_id} ...")

        if not node_ip:
            print(f"No valid node found.")
            return False
            
        await self.session_manager.stop_session(node_ip, session_id)

    async def _list_sessions(self):
        await self.session_manager.list_sessions()

    def _open_entity(self, entity: str, node_id: str):
        node_name = self.handle_node_command(node_id)
        node_ip = self.resource_manager.get_ip_for_resource(node_name)
        urls = {
            'sim': self.sim_utils_mapping[self.sim_name].sim_streaming_url(node_ip),
            'viz': f"http://{node_ip}:9090/?url=ws://{node_ip}:9877",
            'nb': f"http://{node_ip}:8890",
            'code': f"code --folder-uri=vscode-remote://attached-container%2B677269645f636f7265/workspace"
        }

        # Special handling for VSCode URLs
        if entity == 'code':            
            try:
                subprocess.run(["code", "--folder-uri=vscode-remote://attached-container%2B677269645f636f7265/workspace"], check=True)
                print(f"Opening VSCode remote container on node {node_name}")
                return
            except subprocess.SubprocessError as e:
                self.logger.error(f"Failed to open VSCode: {e}", exc_info=True)
                print(f"Failed to open VSCode. Make sure Visual Studio Code is installed.")

        else:
            url = urls.get(entity)
            if url:
                print(f"Opening {entity} from node {node_name} in default browser at {url}")
                webbrowser.open(url)
            else:
                print(f"Unknown entity: {entity}")

def repl():
    GRIDRepl().cmdloop()

if __name__ == "__main__":
    repl()
