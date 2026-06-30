import asyncio
import logging
import time
import httpx
from models import Server

logger = logging.getLogger(__name__)


class HealthChecker:
    def __init__(self, timeout: float = 5.0, degraded_threshold_ms: float = 500.0):
        self.timeout = timeout
        self.degraded_threshold_ms = degraded_threshold_ms

    async def check(self, server: Server) -> Server:
        url = server.health_url()
        start = time.time()

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url)

            elapsed_ms = (time.time() - start) * 1000

            if resp.status_code == 200 and elapsed_ms <= self.degraded_threshold_ms:
                server.status = "UP"
            elif resp.status_code == 200:
                server.status = "DEGRADED"
            else:
                server.status = "DOWN"

        except (httpx.ConnectError, httpx.TimeoutException):
            server.status = "DOWN"

        return server

    async def check_all(self, servers: list[Server]) -> list[Server]:
        return await asyncio.gather(*(self.check(s) for s in servers))
