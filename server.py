import os
import asyncio
from fastapi import FastAPI
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

@app.get("/token")
def get_token():
    api_key = os.getenv("APIvuD6JXMjQGUc")
    api_secret = os.getenv("k8X5Ccfy0TiskonQEZXLrwOiP2AM9PlLcsqL4rXGwFY")
    
    token = (
        api.AccessToken(api_key, api_secret)
        .with_identity("web-user")
        .with_name("User")
        .with_grants(api.VideoGrants(
            room_join=True,
            room="dev-room",
            can_publish=True,
            can_subscribe=True,
        ))
    )

    return {
        "token": token.to_jwt()
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
