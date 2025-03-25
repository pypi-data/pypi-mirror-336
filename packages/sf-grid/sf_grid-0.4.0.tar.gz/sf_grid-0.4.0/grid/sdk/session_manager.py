import os
import json
import sys
import jwt
import asyncio
import httpx
from typing import Dict, List, Optional
from tabulate import tabulate
import logging
import json

from grid.utils.log_formatter import LogFormatter
from grid.sdk.resource_manager import GRIDResourceManager

class GRIDSessionManager:
    def __init__(self, token_data) -> None:
        self.token_data = token_data
        self.user_id = self.token_data["username"]
        self.platform_auth_token = self.generate_jwt_token(True)
        self.session_nodes = {}
        self.nodes = GRIDResourceManager.list_nodes()

        # Configure logging
        self.logger = logging.getLogger('session_manager')
        log_filename = os.path.expanduser('~') + '/.grid/logs/session_manager.log'
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        handler = logging.FileHandler(log_filename)
        handler.setFormatter(LogFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def generate_jwt_token(self, is_platform: bool) -> str:
        return jwt.encode(
            {"user_id": "test_user", "session_id": "test_session"},
            (
                "aksdhiefrifhroihfoih4hfroihofirkshdueuhduihfr"
                if is_platform
                else "aksdhiefrifhroihfoih4hfroihofirade"
            ),
            algorithm="HS512",
        )

    def create_config(self, session_config_file_path: str, session_id: str) -> Dict:
        session_config_file_path = os.path.abspath(os.path.expanduser(session_config_file_path))
        with open(session_config_file_path, 'r') as config_file:
            config_data = json.load(config_file)

        # Check if the required keys exist in the config_data
        if 'sim' not in config_data or 'grid' not in config_data:
            raise ValueError("The session config file must contain 'sim' and 'grid' configuration.")

        config_dict = {
            "user": {"user_id": self.user_id},
            "session": {
                "session_id": session_id,
                "sim": config_data["sim"],
                "grid": config_data["grid"],
            },
        }
        return config_dict

    async def start_session(self, session_id: str, session_config_file_path: str, node_ip: str) -> Optional[bool]:
        """
        Start a session on the specified node.

        Args:
            session_id (str): The ID of the session to start.
            session_config_file_path (str): The path to the session configuration file.
            node_ip (str): The IP address of the node.

        Returns:
            Optional[bool]: True if the session started successfully, False otherwise.
        """

        config = self.create_config(session_config_file_path, session_id)
        self.logger.info("Initializing session", extra={'arguments': {
            'session_id': session_id, 
            'node_ip': node_ip, 
            'sim': config["session"]["sim"]["sim_type"], 
            'scene': config["session"]["sim"]["scene_name"],
            'session_config': config}})

        # Download required assets first

        # Parse the session config to check if "sim" is "airgen"
        sim_config = config["session"]["sim"]
        if sim_config.get("sim_type") == "airgen":
            # Use download_assets from airgen_utils and send it the "env_name"
            print("Downloading assets...")
            from grid.utils.airgen_utils import AirGenUtils
            env_name = sim_config["scene_name"]
            if not AirGenUtils.download_assets(env_name, token=self.token_data["storage_token"]):
                self.logger.error(f"Failed to download assets for environment: {env_name}")
                return False

        async with httpx.AsyncClient(
            base_url=f"http://{node_ip}:8000", timeout=600
        ) as client:
            try:
                response = await client.post(
                    "/start_session",
                    json={"session_config": config},
                    headers={"Authorization": f"Bearer {self.platform_auth_token}"},
                )
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        print(f"{data['msg_type']}: {data['msg_content']}")
                        sys.stdout.flush()  # Ensure the output is flushed immediately
                        if data["msg_type"] == "response_end":
                            if data["success"]:
                                print("Session started successfully.")
                                self.logger.info("Session started successfully.")
                                self.session_nodes[session_id] = node_ip  # Store the mapping
                            else:
                                print("Failed to start session.")
                                self.logger.error(f"Failed to start session.")
                            return data["success"]
            except httpx.RequestError as e:
                print(f"Request error: {e}")
                sys.stdout.flush()  # Ensure the output is flushed immediately
                return None

    async def stop_session(self, node_ip: str, session_id: str) -> bool:
        """
        Terminate a session on the specified node.

        Args:
            session_id (str): The ID of the session to terminate.
            node_ip (str): The IP address of the node.

        Returns:
            Optional[bool]: True if the session terminated successfully, False otherwise.
        """

        self.logger.info("Terminating session", extra={'arguments': {'session_id': session_id, 'node_ip': node_ip}})
        async with httpx.AsyncClient(
            base_url=f"http://{node_ip}:8000", timeout=600
        ) as client:
            try:
                response = await client.post(
                    "/terminate_session",
                    json={"session_id": session_id, "user_id": self.user_id},
                    headers={"Authorization": f"Bearer {self.platform_auth_token}"},
                )
                response_data = response.json()
                if response_data.get("success"):
                    print("Session stopped successfully.")
                    self.logger.info("Session stopped successfully.")
                    if session_id in self.session_nodes:
                        del self.session_nodes[session_id]  # Remove the mapping
                else:
                    print("Failed to stop session.")
                    self.logger.error("Failed to stop session.")
                    print("Response:", response_data)
                return response_data.get("success", False)
            except httpx.RequestError as e:
                print(f"Request error: {e}")
                self.logger.error(f"Request error: {e}")
                return False

    async def list_sessions(self) -> List[Dict]:
        tasks = [self.get_session_info(node["IP Address"]) for node in self.nodes]
        session_info_list = await asyncio.gather(*tasks)
        
        if any(info["session_id"] not in [None, ""] for info in session_info_list):
            headers = ["Session ID", "Node IP", "Last Active Time"]
            table_data = [
                [info["session_id"], info["node_ip"], info["last_active_time"]]
                for info in session_info_list
            ]
            for info in session_info_list:
                if info["session_id"] not in [None, ""] and info["session_id"] not in self.session_nodes:
                    self.session_nodes[info["session_id"]] = info["node_ip"]
                    
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
        else:
            print("No active sessions found.")

        return session_info_list
    
    async def get_session_info(self, node_ip: str, session_id: Optional[str] = None) -> Dict:
        async with httpx.AsyncClient(
            base_url=f"http://{node_ip}:8000", timeout=600
        ) as client:
            try:
                response = await client.get(
                    "/is_idle",
                    headers={"Authorization": f"Bearer {self.platform_auth_token}"},
                )
                data = response.json()
                return {
                    "session_id": data.get("session_id", "N/A"),
                    "node_ip": node_ip,
                    "is_idle": data.get("is_idle", "N/A"),
                    "has_active_session": data.get("has_active_session", False),
                    "last_active_time": data.get("last_active_time", "N/A"),
                }
            except httpx.RequestError as e:
                print(f"Request error while fetching session info: {e}")
                return {
                    "session_id": session_id,
                    "node_ip": node_ip,
                    "is_idle": "Error",
                    "has_active_session": False,
                    "last_active_time": "Error",
                }

    async def get_session_id_by_node(self, node_ip: str) -> Optional[str]:
        session_info = await self.get_session_info(node_ip)
        
        if session_info:
            return session_info["session_id"]
        else:
            return None