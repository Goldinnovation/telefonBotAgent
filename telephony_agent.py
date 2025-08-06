import asyncio
import logging
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool
)
from livekit.plugins import deepgram, openai, cartesia, silero, elevenlabs
from workflow.booking import set_user_profile_info, set_type_appointment, set_user_info, set_user_booking_petStatus_and_time, checks_users_totalInput_before_DBCreation



load_dotenv()
logger = logging.getLogger("telephony-agent")

# Function tools to enhance your agent's capabilities

@function_tool
async def lookup_weather(context: RunContext, location: str):
    return {"weather": "sunny", "temperature": 90, location: "New York"}


# Read the markdown file from the project root
with open("instructions/klara.md", "r", encoding="utf-8") as file:
    klara_instructions = file.read()






async def entrypoint(ctx: JobContext):
    """Main entry point for the telephony voice agent."""
    await ctx.connect()
    
    # Wait for participant (caller) to join
    participant = await ctx.wait_for_participant()
    logger.info(f"Phone call connected from participant: {participant.identity}")
    
    # Initialize the conversational agent
    agent = Agent(
        instructions= klara_instructions,

        tools=[
            function_tool(set_type_appointment,
            name="set_type_appointment",
            description="Rufe diese Funktion auf, wenn der Nutzer dir die Art des Termin und tieres nennt."), 
            function_tool(set_user_info,
            name="set_user_info",
            description="Rufe diese Funktion auf, wenn der Nutzer dir sein Name, Geburtsdatum und Nummer nennt."),
            function_tool(set_user_booking_petStatus_and_time,
            name="set_user_booking_petStatus_and_time",
            description="Rufe diese Funktion auf, wenn der Nutzer die DringlichkeitStatus mitgeteilt und das Datum und die Zeit der Verfügbarkeit bestätigt hat."
            ), 
            function_tool(checks_users_totalInput_before_DBCreation,
            name="checks_users_totalInput_before_DBCreation",
            description="Rufe diese Funktion auf, wenn alle Nutzerdaten geprüft werden sollen oder das Gespräch zu Ende geht."
            ), 

    

        ]
    )
    
    # Configure the voice processing pipeline optimized for telephony

  


    session = AgentSession(

        # print(voices)
        # Voice Activity Detection
        vad=silero.VAD.load(),
        
        # Speech-to-Text - Deepgram Nova-3
        stt=deepgram.STT(
            model="nova-3",  # Latest model
            language="de",
            interim_results=True,
            punctuate=True,
            smart_format=True,
            filler_words=True,
            endpointing_ms=25,
            sample_rate=16000
        ),
        
        # Large Language Model - GPT-4o-mini
        llm=openai.LLM(
            model="gpt-4o-mini",
            temperature=0.5
        ),
        
        # Text-to-Speech - Cartesia Sonic-2
       

        # tts=elevenlabs.TTS(
        #    voice_id="AnvlJBAqSLDzEevYr9Ap",
        #     model="eleven_multilingual_v2"
           
        # )
          tts=openai.TTS(
            voice="shimmer",
            speed=1.1
          ),
    )
    
    # Start the agent session
    await session.start(agent=agent, room=ctx.room)
    
    # Generate personalized greeting based on time of day
    import datetime
    hour = datetime.datetime.now().hour
    if hour < 12:
        time_greeting = "Guten Morgen"
    elif hour < 18:
        time_greeting = "Guten Tag"
    else:
        time_greeting = "Guten Abend"
    
    await session.generate_reply(
        instructions="Begrüße den Benutzer und frage nach seinem namen und geburtstag"
    )

if __name__ == "__main__":
    # Configure logging for better debugging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the agent with the name that matches your dispatch rule
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="telephony_agent"  # This must match your dispatch rule
    ))