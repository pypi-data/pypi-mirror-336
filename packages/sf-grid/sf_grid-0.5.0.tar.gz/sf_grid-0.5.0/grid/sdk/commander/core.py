import paramiko
import subprocess
import shlex
import os
import yaml
import importlib.resources as pkg_resources

class Commander:
    def __init__(self):
        self.node_data = None
        self.sim_profile = None
        self.docker_container_names = ['grid_core', 'grid_server', 'grid_sim']
        self.sims = ['airgen', 'isaac']

        # Construct the path to docker-compose.yml
        with pkg_resources.files('grid.utils').joinpath('docker-compose.yml') as compose_file_path:
            self.docker_compose_file_path = str(compose_file_path)

    def set_node_data(self, data):
        self.node_data = data

    def check_grid_containers(self):
        # Check if all three GRID containers are running
        container_status = {container: self.check_docker_container(container) for container in self.docker_container_names}
        return all(container_status.values())

    def check_docker_container(self, container_name: str) -> bool:
        command = "docker ps --format {{.Names}}"
        output = self.run_command(command, run_quiet=True)

        container_list = output.splitlines() if output else []
        return container_name in container_list

    def get_sim(self):
        return self.sim_profile
    
    def set_sim(self, sim_name):
        self.sim_profile = sim_name
        self.docker_container_names[2] = f"grid_sim_{self.sim_profile}"

    def init_containers(self, volume_info):        
        if volume_info:
            # Load the docker-compose.yml file
            with open(self.docker_compose_file_path, 'r') as file:
                compose_data = yaml.safe_load(file)

            for container_path, host_path in volume_info.items():
                # Add the volume to the grid_core service
                if 'volumes' not in compose_data['services']['core']:
                    compose_data['services']['core']['volumes'] = []
                
                compose_data['services']['core']['volumes'].append(f'{host_path}:/workspace/{container_path}')

                if 'volumes' not in compose_data['services']['sim-airgen']:
                    compose_data['services']['sim-airgen']['volumes'] = []
                
                compose_data['services']['sim-airgen']['volumes'].append(f'{host_path}:/mnt/{container_path}')

            # Write the modified compose data back to the file
            with open(self.docker_compose_file_path, 'w') as file:
                yaml.safe_dump(compose_data, file)
        
        compose_command = f"docker compose -f {self.docker_compose_file_path} --profile {self.sim_profile} up -d"
        
        # Yield the output from the `run_compose_command` method
        for output in self.run_compose_command(compose_command, run_quiet=False):
            yield output  # Stream the command output as-is
        
        yield "Checking container statuses...\n"
        container_status = {image: self.check_docker_container(image) for image in self.docker_container_names}

        for container, status in container_status.items():
            status_symbol = u"\u2713" if status else u"\u274C"
            yield f"{container}: {status_symbol}\n"

        if False in container_status.values():
            yield "Error: One or more GRID containers failed to start. Please check the logs.\n"
        else:
            yield "Containers are active.\n"

    def login_registry(self, username, password):
        """Login to the GRID registry using username and password/access token"""
        yield "Logging in to Scaled Foundations - GRID registry..."

        login_command = f"docker login sfgrid.azurecr.io -u {username} --password-stdin"
        completed_process = subprocess.run(shlex.split(login_command), input=password.encode() + b'\n', capture_output=True)
        if completed_process.returncode == 0:
            yield "Login successful!"
        else:
            yield "Login failed with the following error:"
            yield completed_process.stderr.decode()

    def kill_containers(self):
        yield f"Stopping containers using docker-compose...\n"

        compose_command = f"docker compose -f {self.docker_compose_file_path} --profile \"*\" down"
        
        # Yield the output from the `run_compose_command` method
        for output in self.run_compose_command(compose_command, run_quiet=False):
            yield output  # Stream the command output as-is

        yield "Checking container statuses...\n"
        container_status = {container: self.check_docker_container(container) for container in self.docker_container_names}
        
        for container, status in container_status.items():
            status_symbol = u"\u2713" if status else u"\u274C"
            yield f"{container}: {status_symbol}\n"

        if not True in container_status.values():
            yield "Containers stopped successfully.\n"
        else:
            yield "Error: One or more containers are still active.\n"

    def update_containers(self):
        yield f"Updating containers for profile {self.sim_profile}...\n"
        
        compose_command = f"docker compose -f {self.docker_compose_file_path} --profile {self.sim_profile} pull"
        for output in self.run_compose_command(compose_command, run_quiet=False):
            yield output

    def run_compose_command(self, command: str, run_quiet=False):
        with os.popen(command) as process:
            for line in process:
                if not run_quiet:
                    yield line
        
    def run_command(self, command: str, run_quiet: str = False):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if stdout:
            if not run_quiet:
                print(stdout.strip())
            return stdout
        if stderr:
            print(stderr.strip())

    def run_remote_command(self, resource_name: str, command: str) -> str:
        hostname = self.node_data[resource_name]["ip"]
        username = self.node_data[resource_name]["username"]
        password = self.node_data[resource_name]["password"]

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the remote host
            ssh.connect(hostname, username=username, password=password)

            # Execute the command
            stdin, stdout, stderr = ssh.exec_command(command)

            # Read the output and error streams
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                return f"Error: {error}"
            return output
        except Exception as e:
            return f"Exception: {str(e)}"
        finally:
            # Close the SSH connection
            ssh.close()
