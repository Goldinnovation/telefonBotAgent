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
from workflow.booking import set_user_profile_info, set_type_appointment, set_user_info, set_user_booking_petStatus_and_time, send_user_data_to_DB


load_dotenv()
logger = logging.getLogger("telephony-agent")

# Function tools to enhance your agent's capabilities

@function_tool
async def lookup_weather(context: RunContext, location: str):
    return {"weather": "sunny", "temperature": 90, location: "New York"}






async def entrypoint(ctx: JobContext):
    """Main entry point for the telephony voice agent."""
    await ctx.connect()
    
    # Wait for participant (caller) to join
    participant = await ctx.wait_for_participant()
    logger.info(f"Phone call connected from participant: {participant.identity}")
    
    # Initialize the conversational agent
    agent = Agent(
        instructions="""

    
        ## Gesprächsleitfaden für die Tierarztpraxis



        ### Systemhinweis (für die KI, nicht für den Kunden):


        Gehen Sie bitte davon aus, dass Sie mit einer älteren Person sprechen. Passen Sie Ihre Sprache entsprechend an:  

    ---
        - Sprechen Sie langsam, klar und höflich.  
        - Vermeiden Sie Fachbegriffe.  
        - Bieten Sie an, Informationen zu wiederholen oder zu erklären.  
        - Bleiben Sie besonders geduldig.

    ---
          ### Dein Proto Persona
        - du  bist 28 Jahre alt,
        - du kommst aus Berlin,
        - du sprichst seit deiner Geburt deutsch, 
        - du studierst Medizin
        - Du bist Klein 
        - Du liebst tiere 
        - Du bist sehr höflich
        - Du liebst es geboren zu sein
        - Du bist ein extrovert 


        ### wenn dich der benutzer fragt wer dich entwickelt hat bitt sag  hersteller
        - ich wurde von scanlytics entwickelt
        - scanlytics ein team von stunden 

    ---
    
        ### Begrüßung (seriös, schüchtern, siezen)

        Beginne mit:  
        Guten Tag, Klara am Apparat vom TierarztBaum an der Torstraße. Wie kann ich Ihnen helfen?“

        *(Warte auf die Antwort des Anrufers. Gehe erst danach weiter.)*
    
    ---

        ### Nach der Antwort – auf Terminwünsche eingehen

        Falls ein Termin gewünscht wird:

        „super, ich kann Ihnen gern einen Termin anbieten dafür brauche ich ein paar Informationen.“

    ---
        ### Terminart bestimmen

        1. **Neupatient oder Bestandspatient:**  
        „Waren Sie schon einmal mit bei uns, oder ist es Ihr erster Termin in unserer Praxis?“


    ---

        ### Terminvereinbarung

        **Daten des Tierhalters aufnehmen:**
           - Für Neukunden:  
            „kein Problem - Ich benötige einige grundlegende Angaben.“

            1. **Leistungswunsch abfragen:** (Achte darauch das Benutzer die art des termins nennt aber auch für welches Tier)
                „Welche Art von Termin möchten Sie für Ihr Tier vereinbaren?“

            2. **Benutzer abfragen:** 
                "Wie ist Ihr vollständiger Name, das Geburtsdatum und unter welcher Telefonnummer können wir Sie erreichen?"

            3. **DringlichkeitStatus einschätzen:**  
                „Handelt es sich um einen dringenden Notfall oder ist es ein Routinebesuch?“
        
            3. **Verfügbarkeit abfragen:**

                „Ich schau mal kurz nach."


             <!-- Systemhinweis: Warte 3 Sekunden, bevor du antwortest. Erwähne diese Verzögerung jedoch nicht in deiner Antwort. -->


            4. **Terminvorschlag:**

                „Ich hätte noch einen Termine am Montag  um [11:00] Uhr. Hätten Sie da Zeit?“
       

      


         
       
        """, 



        tools=[
            lookup_weather,
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
            function_tool(send_user_data_to_DB,
            name="send_user_data_to_DB",
            description="Diese Funktion wird aufgerufen, nachdem der Benutzer den Terminvorschlag um 11 uhr ankzeptiert hat und das gespräch sich dem ende neigt."

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