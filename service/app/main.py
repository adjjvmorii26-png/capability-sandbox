from fastapi import FastAPI
from pydantic import BaseModel
import time, uuid
from capability_policy import sign_token

app = FastAPI(title="Capability Token Service")

class MintRequest(BaseModel):
    agent_id: str
    capabilities: dict
    ttl_seconds: int = 60

@app.post("/mint")
def mint(req: MintRequest):
    now = int(time.time())
    token = {
        "token_id": f"cap_{uuid.uuid4().hex[:8]}_{now}",
        "issuer": "orchestrator",
        "agent_id": req.agent_id,
        "issued_at": now,
        "expires_at": now + req.ttl_seconds,
        "capabilities": req.capabilities,
        "metadata": {}
    }
    token["signature"] = sign_token(token, b"replace_with_secret")
    return token