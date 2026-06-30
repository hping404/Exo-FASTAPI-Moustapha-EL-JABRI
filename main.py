import logging
from fastapi import FastAPI, HTTPException
from models import Server, ServerIn, ServerOut
from health import HealthChecker

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="DevOps Monitoring API", version="1.0")

_store: dict[int, Server] = {}
_counter = 0

checker = HealthChecker()


@app.get("/health")
async def api_health():
    return {"status": "ok", "servers_monitored": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201)
async def create_server(server: ServerIn):
    global _counter
    _counter += 1

    obj = Server(
        id=_counter,
        name=server.name,
        host=server.host,
        port=server.port,
        protocol=server.protocol,
        health_path=server.health_path,
        tags=server.tags,
    )

    _store[_counter] = obj
    return obj


@app.get("/servers", response_model=list[ServerOut])
async def list_servers(status: str | None = None):
    servers = list(_store.values())

    if status:
        servers = [s for s in servers if s.status == status]

    return servers


@app.get("/servers/{server_id}", response_model=ServerOut)
async def get_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(404, "Server not found")
    return _store[server_id]


@app.delete("/servers/{server_id}", status_code=204)
async def delete_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(404, "Server not found")
    del _store[server_id]


@app.post("/servers/{server_id}/check", response_model=ServerOut)
async def check_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(404, "Server not found")

    server = await checker.check(_store[server_id])
    return server
