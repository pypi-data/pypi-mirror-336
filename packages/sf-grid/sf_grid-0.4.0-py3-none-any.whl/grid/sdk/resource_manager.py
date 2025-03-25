class GRIDResourceManager:
    host_grid_local = True
    resource_config = {}

    def __init__(self, resource_config):
        GRIDResourceManager.resource_config = resource_config

        try:
            if "host_grid_local" in GRIDResourceManager.resource_config:
                GRIDResourceManager.host_grid_local = GRIDResourceManager.resource_config["host_grid_local"]
                del GRIDResourceManager.resource_config["host_grid_local"]
        except KeyError:
            raise KeyError("Key 'host_grid_local' not found in resource config. Please specify whether GRID containers should be hosted locally.")
    
    @staticmethod
    def list_nodes():
        if not GRIDResourceManager.resource_config:
            print("No nodes found in the configuration.")
            return

        node_list = [{"Node Name": node, "IP Address": details["ip"]} for node, details in GRIDResourceManager.resource_config.items()]
        return node_list
            

    @staticmethod
    def get_resource_config():
        return GRIDResourceManager.resource_config

    @staticmethod
    def get_ip_for_resource(resource_name: str):
        if not GRIDResourceManager.resource_config.get(resource_name):
            raise ValueError(f"Resource {resource_name} not found in resource config.")
        else:
            return GRIDResourceManager.resource_config[resource_name]["ip"]
        
    @staticmethod
    def get_storage_mount_info(resource_name: str):
        if not GRIDResourceManager.resource_config.get(resource_name):
            raise ValueError(f"Resource {resource_name} not found in resource config.")
        else:
            resource_info = GRIDResourceManager.resource_config[resource_name]
            if "storage" in resource_info and resource_info["storage"]:
                storage_volumes = resource_info["storage"]
                return storage_volumes
            else:
                return {}