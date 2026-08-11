import aioredis, json, time
STREAM="tasks"; GROUP="agents_group"
class RedisBus:
    def __init__(self, url="redis://redis:6379/0"):
        self.url = url; self.redis = None
    async def connect(self):
        self.redis = await aioredis.from_url(self.url, decode_responses=True)
        try: await self.redis.xgroup_create(STREAM, GROUP, id="$", mkstream=True)
        except: pass
    async def post_task(self, payload):
        return await self.redis.xadd(STREAM, {"payload": json.dumps(payload), "created_at": str(time.time())})
    async def claim_task(self, consumer, block_ms=1000):
        res = await self.redis.xreadgroup(GROUP, consumer, {STREAM: ">"}, count=1, block=block_ms)
        if not res: return None
        _, messages = res[0]; msg_id, fields = messages[0]
        return {"id": msg_id, "payload": json.loads(fields["payload"])}
    async def ack_task(self, task_id, result):
        await self.redis.xack(STREAM, GROUP, task_id)
        await self.redis.hset(f"task_result:{task_id}", mapping={"result": json.dumps(result), "ts": str(time.time())})
    async def fail_task(self, task_id, reason):
        await self.redis.xack(STREAM, GROUP, task_id)
        await self.redis.xadd("dead_letter", {"task_id": task_id, "reason": reason, "ts": str(time.time())})