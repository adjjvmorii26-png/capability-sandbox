import asyncio, logging
logger = logging.getLogger("agent")

class BaseAgent:
    def __init__(self, agent_id, bus):
        self.agent_id = agent_id
        self.bus = bus

    async def start(self):
        while True:
            task = await self.bus.claim_task(self.agent_id)
            if not task:
                await asyncio.sleep(0.1)
                continue
            try:
                result = await self.handle(task["payload"])
                await self.bus.ack_task(task["id"], result)
            except Exception as e:
                await self.bus.fail_task(task["id"], str(e))

    async def handle(self, payload):
        raise NotImplementedError