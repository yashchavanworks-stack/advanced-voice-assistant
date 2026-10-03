import os
import asyncio
from dotenv import load_dotenv
from livekit import agents, api
from livekit.agents import llm
from livekit.plugins import openai

load_dotenv()

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
    await assistant.say("Hello! How can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    if api_key and api_secret:
        token = api.AccessToken(api_key, api_secret)\
            .with_identity("web_user")\
            .with_grants(api.VideoGrants(room_join=True, room="dev-room"))
        print("\n" + "="*60)
        print("YOUR TEMPORARY TESTING TOKEN:")
        print(token.to_jwt())
        print("="*60 + "\n")
        
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
