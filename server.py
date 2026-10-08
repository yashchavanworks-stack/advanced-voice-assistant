import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from livekit import api
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok", "service": "token-server"}

@app.post("/token")
async def get_token(request: Request):
    body = await request.json()

    api_key = os.getenv("APIvuD6JXMjQGUc")
    api_secret = os.getenv("k8X5Ccfy0TiskonQEZXLrwOiP2AM9PlLcsqL4rXGwFY")
    livekit_url = os.getenv("wss://voice-assistant-psxcd808.livekit.cloud")

    if not all([api_key, api_secret, livekit_url]):
        return {"error": "Missing LiveKit credentials"}, 500

    room_name = body.get("room_name") or "voice-room"
    identity = body.get("participant_identity") or "web-user"
    name = body.get("participant_name") or "User"

    token = (
        api.AccessToken(api_key, api_secret)
        .with_identity(identity)
        .with_name(name)
        .with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        ))
    )

    return {
        "server_url": livekit_url,
        "participant_token": token.to_jwt(),
        "room_name": room_name,
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)