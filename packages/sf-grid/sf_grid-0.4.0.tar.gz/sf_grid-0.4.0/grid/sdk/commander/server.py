from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from grid.sdk.commander.core import Commander
import threading
import uvicorn
import logging

# Suppress uvicorn logging
logging.getLogger("uvicorn").setLevel(logging.CRITICAL)

app = FastAPI()
commander = Commander()

class LoginCredentials(BaseModel):
    username: str
    password: str

class NodeData(BaseModel):
    data: dict

class NodeName(BaseModel):
    node_name: str

class SimName(BaseModel):
    sim_name: str

class VolumeInfo(BaseModel):
    volume_info: dict

@app.post("/set_node_data/")
def set_node_data(data: NodeData):
    commander.set_node_data(data.data)
    return {"message": "Node data set successfully"}

@app.post("/set_node_name/")
def set_node_name(node_name: NodeName):
    commander.set_node_name(node_name.node_name)
    return {"message": "Node name set successfully"}

@app.post("/set_sim/")
def set_sim(sim_name: SimName):
    commander.set_sim(sim_name.sim_name)
    return {"message": "Simulation profile set successfully"}

@app.get("/get_sim/")
def get_sim():
    sim_name = commander.get_sim()
    return {"sim_name": sim_name}

@app.post("/init_containers/")
def init_containers(volume_info: VolumeInfo):
    return StreamingResponse(commander.init_containers(volume_info.volume_info), media_type="text/plain")

@app.post("/login_registry/")
def login_registry(credentials: LoginCredentials):
    username = credentials.username
    password = credentials.password
    return StreamingResponse(commander.login_registry(username, password), media_type="text/plain")

@app.post("/kill_containers/")
def kill_containers():
    return StreamingResponse(commander.kill_containers(), media_type="text/plain")

@app.post("/update_containers/")
def update_containers():
    return StreamingResponse(commander.update_containers(), media_type="text/plain")

@app.get("/check_containers/")
def check_containers():
    container_status = commander.check_grid_containers()
    return JSONResponse(content={"status": container_status})

class CommanderServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8060):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            print("Container server is already running.")
            return

        # Uvicorn configuration
        config = uvicorn.Config(
            app=app,
            host=self.host,
            port=self.port,
            log_level="critical",
        )
        self.server = uvicorn.Server(config)

        # Create and start a new thread that runs uvicorn
        self.thread = threading.Thread(target=self.server.run, daemon=False)

        print(f"Started container server on {self.host}:{self.port}")
        self.thread.start()

    def stop(self):
        if self.server is not None:
            print("Stopping the container server...")
            self.server.should_exit = True
        if self.thread is not None:
            self.thread.join()
            print("Container server stopped.")

if __name__ == "__main__":
    server = CommanderServer()