"""
Voice AI assistant using LiveKit for collecting patient info and scheduling appointments.
Integrates with OpenAI, Deepgram, Cartesia, and Twilio.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, cartesia, deepgram, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.agents import function_tool, get_job_context, RunContext
from emailing import send_summary_email
from constants import PATIENT_INFO_TEMPLATE, LLM_INSTRUCTIONS
from handlers import set_patient_field, get_available_doctors, get_available_times, final_review, hangup_call

load_dotenv()

patient_info = PATIENT_INFO_TEMPLATE

# TODO: In a real application, this would be replaced with a proper database or API call
def verify_address(address: str) -> bool:
    return True

class Assistant(Agent):
    def __init__(self) -> None:
        # tools are defined in handlers.py
        tools = [set_patient_field(field, patient_info) for field in PATIENT_INFO_TEMPLATE.keys()] + [
            get_available_doctors(),
            get_available_times(),
            final_review(patient_info),
            ]
        super().__init__(instructions=LLM_INSTRUCTIONS, tools=tools)
        
    @function_tool
    async def end_call(self, ctx: RunContext):
        """Called when the user wants to end the call"""
        current_speech = ctx.session.current_speech
        if current_speech:
            await current_speech.wait_for_playout()

        await hangup_call()

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVCTelephony(), 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )

    async def my_shutdown_hook():
        print("[DEBUG] Ending session, sending email...")
        send_summary_email(patient_info)

    ctx.add_shutdown_callback(my_shutdown_hook)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint
    ))