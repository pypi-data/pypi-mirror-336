from .azcopy_downloader import AzCopyDownloader
import os 
from typing import Dict

class AirGenUtils:
    @staticmethod
    def download_assets(env_name: str, token: str) -> bool:
        """
        Downloads the specified environment assets using AzCopyDownloader.

        :param env_name: The name of the environment to download.
        :return: True if download is successful, False otherwise.
        """
        downloader = AzCopyDownloader()
        container_url = f"https://gridenterpriseresources.blob.core.windows.net/airgenbins/{env_name}.tar"  # Replace with actual URL
        destination_path = os.path.expanduser(f"~/.grid/airgenbins/{env_name}.tar")

        return downloader.download_asset(container_url, token, destination_path)
    
    @staticmethod
    def post_init(token: str, force_redownload: bool = False) -> bool:
        return True
    
    @staticmethod
    def sim_streaming_url(node_ip: str) -> str:
        return f"http://{node_ip}:3080"
    
    @staticmethod
    def create_sample_config() -> Dict:
        sample_session_config = {
            "sim": {
                "sim_type": "airgen",
                "scene_name": "blocks",
                "kwargs": {
                    "geo": False,
                },
                "settings": {
                    "SimMode": "Car",
                "Vehicles": {
                    "Drone": {
                        "VehicleType": "Chaos",
                        "VehicleModel": "MCR"
                    }
                    },
                    "OriginGeopoint": {
                    "Latitude": 47.62094998919241,
                    "Longitude": -122.35554810901883,
                    "Altitude": 100
                    }
                }
                },
                "grid": {
                "entities": {
                    "robot": [{"name": "airgen-drone", "kwargs": {}}],
                    "model": []
                }
            }
        }

        return sample_session_config
