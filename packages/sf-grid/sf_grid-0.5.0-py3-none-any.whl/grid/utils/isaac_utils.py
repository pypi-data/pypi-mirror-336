from .azcopy_downloader import AzCopyDownloader
import os 
from typing import Dict

class IsaacUtils:
    @staticmethod
    def download_assets(env_name: str, token: str, force_redownload: bool = False) -> bool:
        """
        Downloads the specified environment assets using AzCopyDownloader.

        :param env_name: The name of the environment to download.
        :return: True if download is successful, False otherwise.
        """
        downloader = AzCopyDownloader()
        container_url = f"https://gridenterpriseresources.blob.core.windows.net/isaac/{env_name}"  # Replace with actual URL
        destination_path = os.path.expanduser(f"~/.grid/isaac")

        return downloader.download_asset(container_url, token, destination_path, force_redownload=force_redownload)
    
    @staticmethod
    def post_init(token: str, force_redownload: bool = False) -> bool:
        env_name = "common"
        if not IsaacUtils.download_assets(env_name, token=token, force_redownload=force_redownload):
            return False
        
        return True
    
    @staticmethod
    def sim_streaming_url(node_ip: str) -> str:
        return f"http://{node_ip}:3080"
    
    @staticmethod
    def create_sample_config() -> Dict:
        sample_session_config = { 
            "sim": {
                "sim_type": "isaac",
                "scene_name": "isaac_tabletop",
                "kwargs": {
                "geo": False,
                },
                "settings": {
                    "robot_name": "isaac_franka_kb",
                },
            },
            "grid": {
                "entities": {
                    "robot": [
                        {
                            "name": "arm:isaac:sim",
                            "kwargs": {}
                        }
                    ],
                    "model": [], 
                },
            }
        }

        return sample_session_config