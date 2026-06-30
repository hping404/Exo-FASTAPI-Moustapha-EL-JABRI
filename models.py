from dataclasses import dataclass, field
from pydantic import BaseModel, Field


@dataclass
class Server:
    """Internal server representation."""
    id: int
    name: str
    host: str
    port: int
    protocol: str = "http"
    health_path: str = "/health"
    status: str = "unknown"
    tags: list[str] = field(default_factory=list)

    def base_url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"

    def health_url(self) -> str:
        return f"{self.base_url()}{self.health_path}"


class ServerIn(BaseModel):
    name: str
    host: str
    port: int = Field(default=8080, ge=1, le=65535)
    protocol: str = "http"
    health_path: str = "/health"
    tags: list[str] = []


class ServerOut(BaseModel):
    id: int
    name: str
    host: str
    port: int
    protocol: str
    health_path: str
    status: str
    tags: list[str] = []

    model_config = {"from_attributes": True}
