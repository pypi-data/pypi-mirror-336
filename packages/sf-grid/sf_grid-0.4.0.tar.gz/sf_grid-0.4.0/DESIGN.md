# GRID SDK Design Document

## Overview

The GRID SDK provides access to the General Robot Intelligence Development Enterprise platform. GRID is a platform for rapid infusion of AI into robotic platforms built by Scaled Foundations. This document explains the overall architecture, setup, and the most relevant API descriptions across the files in the project.

## Project Structure

### Components

Each component in the GRID SDK serves a specific purpose, facilitating the management and orchestration of AI-driven robotic platforms.

1. **REPL (Read-Eval-Print Loop)**
    - **File**: `repl.py`
    - **Class**: `GRIDRepl`
    - **Description**: The REPL is the main entry point for interacting with the GRID platform. It provides a command-line interface for managing nodes, sessions, and containers.
    - **Reason for Existence**: To provide users with an interactive shell to control and manage the GRID platform.
    - **Key Methods**:
      - `do_login(arg)`: Logs in to the GRID platform registry.
      - `do_init(arg)`: Initializes the GRID containers.
      - `do_terminate(arg)`: Terminates the GRID containers.
      - `do_update(arg)`: Updates the GRID containers.
      - `do_node(arg)`: Manages nodes (e.g., lists all nodes).
      - `do_session(arg)`: Manages sessions (e.g., starts, stops, lists sessions).
      - `do_open(arg)`: Opens an entity (notebook, simulation, or telemetry).
      - `do_exit(arg)`: Exits the REPL.
      - `do_help(arg)`: Displays help information for REPL commands.
      - `do_license(arg)`: Displays the license information.

2. **Commander**
    - **Files**: `core.py`, `client.py`, `server.py`
    - **Classes**: `Commander`, `CommanderClient`, `CommanderServer`
    - **Description**: The Commander is responsible for managing Docker containers and executing commands on remote nodes.
    - **Reason for Existence**: To handle the orchestration of Docker containers and facilitate remote command execution.
    - **Key Methods**:
      - `Commander.init_containers()`: Initializes Docker containers using docker-compose.
      - `Commander.kill_containers()`: Stops Docker containers using docker-compose.
      - `Commander.update_containers()`: Updates Docker containers using docker-compose.
      - `CommanderClient.init_containers(node_name)`: Initializes containers on a specified node.
      - `CommanderClient.kill_containers(node_name)`: Kills containers on a specified node.
      - `CommanderServer.start()`: Starts the FastAPI server for container orchestration.

3. **Session Manager**
    - **File**: `session_manager.py`
    - **Class**: `GRIDSessionManager`
    - **Description**: The Session Manager handles the lifecycle of sessions, including starting, stopping, and listing sessions.
    - **Reason for Existence**: To manage the lifecycle of sessions, ensuring that sessions are properly started, stopped, and tracked.
    - **Key Methods**:
      - `start_session(session_id, session_config_file_path, node_ip)`: Starts a session on a specified node.
      - `stop_session(node_ip, session_id)`: Stops a session on a specified node.
      - `list_sessions()`: Lists all active sessions.

4. **Resource Manager**
    - **File**: `resource_manager.py`
    - **Class**: `GRIDResourceManager`
    - **Description**: The Resource Manager manages the configuration and IP addresses of resources (nodes).
    - **Reason for Existence**: To handle the configuration and retrieval of resource information, such as IP addresses.
    - **Key Methods**:
      - `get_ip_for_resource(resource_name)`: Retrieves the IP address for a specified resource.

5. **Utilities**
    - **Files**: `airgen_utils.py`, `asset_downloader.py`, `config_handler.py`, `isaac_utils.py`, `docker-compose.yml`
    - **Description**: Utilities provide helper functions and classes for various tasks, such as downloading assets and handling configurations.
    - **Reason for Existence**: To provide common utility functions that support the main components of the GRID SDK.
    - **Key Classes and Methods**:
      - `AssetDownloader`: Downloads assets using AzCopy.
         - `ensure_azcopy_exists()`: Ensures AzCopy is downloaded and available.
         - `download_asset(container_url, sas_token, destination_path)`: Downloads a file from an Azure container.
      - `ConfigHandler`: Handles loading and saving configuration files.
         - `load_resource_config()`: Loads the resource configuration from a JSON file.
      - `AirGenUtils` and `IsaacUtils`: Provide utility functions for specific simulators.
         - `create_sample_config()`: Creates a sample configuration for the simulator.
         - `sim_streaming_url(node_ip)`: Returns the streaming URL for the simulator.

## API Descriptions

### REPL API

- **Command**: `init simname @nodename`
  - **Description**: Initializes the GRID containers on the specified node.
  - **Example**: `init airgen @local`

- **Command**: `terminate @nodename`
  - **Description**: Terminates the GRID containers on the specified node.
  - **Example**: `terminate @local`

- **Command**: `update @nodename`
  - **Description**: Updates the GRID containers on the specified node.
  - **Example**: `update @local`

- **Command**: `node list`
  - **Description**: Lists all nodes with their IP addresses.
  - **Example**: `node list`

- **Command**: `session start <session_id> <config_path> @<resource_name>`
  - **Description**: Starts a session with the specified configuration on the specified node.
  - **Example**: `session start session1 ~/.grid/config.json @local`

- **Command**: `session stop <session_id>`
  - **Description**: Stops the specified session.
  - **Example**: `session stop session1`

- **Command**: `session list`
  - **Description**: Lists all active sessions.
  - **Example**: `session list`

- **Command**: `open <entity>`
  - **Description**: Opens an entity (notebook, simulation, or telemetry).
  - **Example**: `open notebook`

- **Command**: `close <entity>`
  - **Description**: Closes an open entity.
  - **Example**: `close notebook`

- **Command**: `status`
  - **Description**: Provides the status of the GRID system.
  - **Example**: `status`

- **Command**: `help`
  - **Description**: Displays help information for REPL commands.
  - **Example**: `help`

### Commander API

- **Endpoint**: `POST /set_sim/`
  - **Description**: Sets the simulation profile.
  - **Payload**: `{"sim_name": "airgen"}`

- **Endpoint**: `POST /init_containers/`
  - **Description**: Initializes Docker containers using docker-compose.

- **Endpoint**: `POST /kill_containers/`
  - **Description**: Stops Docker containers using docker-compose.

- **Endpoint**: `POST /update_containers/`
  - **Description**: Updates Docker containers using docker-compose.

- **Endpoint**: `GET /check_containers/`
  - **Description**: Checks the status of Docker containers.

### Session Manager API

- **Method**: `start_session(session_id, session_config_file_path, node_ip)`
  - **Description**: Starts a session on the specified node.
  - **Parameters**:
     - `session_id`: The ID of the session.
     - `session_config_file_path`: The path to the session configuration file.
     - `node_ip`: The IP address of the node.

- **Method**: `stop_session(node_ip, session_id)`
  - **Description**: Stops a session on the specified node.
  - **Parameters**:
     - `node_ip`: The IP address of the node.
     - `session_id`: The ID of the session.

- **Method**: `list_sessions()`
  - **Description**: Lists all active sessions.

### Resource Manager API

- **Method**: `get_ip_for_resource(resource_name)`
  - **Description**: Retrieves the IP address for a specified resource.
  - **Parameters**:
     - `resource_name`: The name of the resource.

### Utilities API

- **Class**: `AssetDownloader`
  - **Method**: `ensure_azcopy_exists()`
     - **Description**: Ensures AzCopy is downloaded and available.
  - **Method**: `download_asset(container_url, sas_token, destination_path)`
     - **Description**: Downloads a file from an Azure container.
     - **Parameters**:
        - `container_url`: The URL of the Azure container.
        - `sas_token`: The SAS token for authentication.
        - `destination_path`: The local path where the file should be downloaded.

- **Class**: `ConfigHandler`
  - **Method**: `load_resource_config()`
     - **Description**: Loads the resource configuration from a JSON file.

- **Class**: `AirGenUtils` and `IsaacUtils`
  - **Method**: `create_sample_config()`
     - **Description**: Creates a sample configuration for the simulator.
  - **Method**: `sim_streaming_url(node_ip)`
     - **Description**: Returns the streaming URL for the simulator.
     - **Parameters**:
        - `node_ip`: The IP address of the node.

## Conclusion

This design document provides an overview of the GRID SDK project, its components, and the most relevant API descriptions. The REPL serves as the main entry point for interacting with the GRID platform, while the Commander, Session Manager, Resource Manager, and Utilities provide the necessary functionality for managing nodes, sessions, and containers.
