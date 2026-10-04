import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from livekit import agents, api
from livekit.agents import llm
from livekit.plugins import openai
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

@app.get("/token")
def get_token():
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    token = api.AccessToken(api_key, api_secret)\
        .with_identity("web_user")\
        .with_grants(api.VideoGrants(room_join=True, room="dev-room"))
    
    return {"token": token.to_jwt()}

async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()
    
    initial_chat_ctx = llm.ChatContext().append(
        role="system",
        text="You are a highly advanced web voice assistant. Keep your answers concise, natural, and conversational.",
    )

    assistant = agents.pipeline.VoicePipelineAgent(
        vad=openai.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_chat_ctx,
    )

    assistant.start(ctx.room)
    await assistant.say("Hello! Welcome to the live website assistant. How can I help you?", allow_interruptions=True)

def start_worker():
    import threading
    loop = asyncio.new_event_loop()
    threading.Thread(target=loop.run_forever, daemon=True).start()
    asyncio.run_coroutine_threadsafe(
        agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint)), 
        loop
    )

if __name__ == "__main__":
    start_worker()
    uvicorn.run(app, host="0.0.0.0", port=8080)
