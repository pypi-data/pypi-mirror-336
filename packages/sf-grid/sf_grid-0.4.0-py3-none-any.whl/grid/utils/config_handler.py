import os 
import json

class ConfigHandler:
    def __init__(self):
        pass

    @staticmethod
    def load_resource_config():
        resource_config_path = os.path.expanduser('~') + '/.grid/resource_config.json'
        if not os.path.exists(resource_config_path):
            os.makedirs(os.path.dirname(resource_config_path), exist_ok=True)
            user_name = input("Enter your username: ")
            password = input("Enter your password: ")
            storage_token = input("Enter your storage token: ")
            with open(resource_config_path, 'w') as f:
                json.dump({"tokens": {"username": user_name, "password": password, "storage_token": storage_token}, "resources": {"host_grid_local": True, "local": {"ip": "localhost"}}}, f)
                print("Resource configuration file created successfully.")

        print(f"Loading resource configuration from {resource_config_path}...")

        with open(resource_config_path) as f:
            resource_config = json.load(f)

        if 'tokens' not in resource_config:
            raise ValueError("The resource config file must contain 'tokens'.")
        else:
            token_data = resource_config['tokens']

        if 'resources' not in resource_config:
            print("No machine config specified in resource configuration. GRID will use localhost by default.")
            resource_data = {"local": {"ip": "localhost"}}
        else:
            resource_data = resource_config['resources']

        return token_data, resource_data