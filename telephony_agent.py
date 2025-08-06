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

load_dotenv()
logger = logging.getLogger("telephony-agent")

# Function tools to enhance your agent's capabilities

@function_tool
async def lookup_weather(context: RunContext, location: str):
    return {"weather": "sunny", "temperature": 90, location: "New York"}


@function_tool
def set_user_profile_info(field: str):
    async def set_birtday_date(conext: RunContext, value: str):
        print(f'called birtday is {value}')
        return f'the field{field} was set to {value}'

    return set_birtday_date
   

    


async def entrypoint(ctx: JobContext):
    """Main entry point for the telephony voice agent."""
    await ctx.connect()
    
    # Wait for participant (caller) to join
    participant = await ctx.wait_for_participant()
    logger.info(f"Phone call connected from participant: {participant.identity}")
    
    # Initialize the conversational agent
    agent = Agent(
        instructions="""

        ### Introduction
            Beginne mit satz :
           Hallo, hier spricht Klara. Mit wem spreche ich?
            (Warte auf die Antwort.)
            Schön, Sie kennenzulernen, [Name]. Darf ich auch noch nach Ihrem Geburtstag fragen?

        ### Personality
        - du bist eine ältere dame und höflich lieb und schüchtern,
        - dutze den benutzer
        - beachte du sprichst mit einem kleinen kind 
        - verspielt
        - Vermittle eine hilfsbereite und geduldige Haltung, besonders gegenüber älteren oder verwirrten Anrufern
        - Bewahre während des gesamten Gesprächs einen warmen ton 
        - Maintain a warm but professional tone throughout the conversation


        ### wenn dich der benutzer fragt wer dich entwickelt hat bitt sag  hersteller
        - ich wurde von scanlytics entwickelt
        - scanlytics ein team von stunden 
        


         ### Speech Characteristics
       
        """, 



        tools=[
            lookup_weather,
            function_tool(set_user_profile_info("geburtstag"),
            name="set_birthday_date",
            description="Rufe diese Funktion auf, wenn der Nutzer dir sein Geburtsdatum nennt.")
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
            temperature=0.7
        ),
        
        # Text-to-Speech - Cartesia Sonic-2
       

        # tts=elevenlabs.TTS(
        #    voice_id="AnvlJBAqSLDzEevYr9Ap",
        #     model="eleven_multilingual_v2"
           
        # )
          tts=openai.TTS(voice="nova"),
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