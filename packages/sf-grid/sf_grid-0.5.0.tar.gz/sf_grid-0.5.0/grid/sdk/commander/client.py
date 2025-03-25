import requests
from grid.sdk.resource_manager import GRIDResourceManager

class CommanderClient:
    def __init__(self):
        pass

    def check_grid_containers(self, node_name):
        node_ip = GRIDResourceManager.get_ip_for_resource(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.get(f"{base_url}/check_containers/")
        response.raise_for_status()
        containers_status = response.json()
        all_up = containers_status.get("status", False)
        return all_up

    def set_sim(self, node_name, sim_name):
        node_ip = GRIDResourceManager.get_ip_for_resource(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.post(f"{base_url}/set_sim/", json={"sim_name": sim_name})
        response.raise_for_status()
        return response.json()
    
    def get_sim(self, node_name):
        node_ip = GRIDResourceManager.get_ip_for_resource(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.get(f"{base_url}/get_sim/")
        response.raise_for_status()
        sim_data = response.json()
        return sim_data.get("sim_name", "")

    def init_containers(self, node_name):
        node_ip = GRIDResourceManager.get_ip_for_resource(node_name)
        volume_info = GRIDResourceManager.get_storage_mount_info(node_name)

        json_data = {"volume_info": volume_info}
        base_url = f"http://{node_ip}:8060"

        response = requests.post(f"{base_url}/init_containers/", json=json_data, stream=True)

        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))

    def login_registry(self, node_name, username, password):
        node_ip = GRIDResourceManager.get_ip_for_resource(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.post(f"{base_url}/login_registry/", json={"username": username, "password": password})
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))

    def kill_containers(self, node_name):
        node_ip = GRIDResourceManager.get_ip_for_resource(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.post(f"{base_url}/kill_containers/", stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))

    def update_containers(self, node_name):
        node_ip = GRIDResourceManager.get_ip_for_resource(node_name)
        base_url = f"http://{node_ip}:8060"
        response = requests.post(f"{base_url}/update_containers/", stream=True)
        response.raise_for_status()
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))