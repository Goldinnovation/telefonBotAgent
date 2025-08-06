
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


patientenDaten = {
    "Name": "",
    "Geburtstag":"", 
    "Nummer":"", 
    "Dringlichkeit":"",
    "Untersuchung":"", 
    "Tier": "",
    "Termin": ""

}

@function_tool
def set_user_profile_info(field: str):
    async def set_birtday_date(conext: RunContext, value: str):
        print(f'called birtday is {value}')
        return f'the field{field} was set to {value}'

    return set_birtday_date
   






# Gets the type of appointment 
@function_tool
async def set_type_appointment(context: RunContext, untersuchung: str, tier:str):
    print(f'Art des Termin und für wen  {untersuchung}')
    print(f'tier des patienten  {tier}')


    patientenDaten["Untersuchung"] = untersuchung
    patientenDaten["Tier"] = tier

    return f'wurde erfolgreich eingetragen'

   



@function_tool
async def set_user_info(context: RunContext, name: str, geburtstag: str, nummer: str ):
    print(f'name: {name}')
    print(f'geburtstag: {geburtstag}')
    print(f'numner {nummer}')

    patientenDaten["Name"] = name
    patientenDaten["Geburtstag"] = geburtstag
    patientenDaten["Nummer"] = nummer



    return f'Super sie sind jetzt im system.'



@function_tool
async def set_user_booking_petStatus_and_time(context: RunContext, dringlichkeit: str, termin:str):
    print(f'DringlichkeitStatus {dringlichkeit}')
    print(f'Zeit {termin}')

    patientenDaten["Dringlichkeit"] = dringlichkeit
    patientenDaten["Termin"] = termin
  


    return f'Super ich hab information eingetragen sind jetzt im system.'

     




@function_tool
async def checks_users_totalInput_before_DBCreation(context: RunContext, nutzerdaten:str):

    """
    Checks which patient data fields are missing and returns appropriate messages.
    If all data is present, creates a DB record.
    """

    print("checks_users_totalInput_before_DBCreation is executed")
    print("Nutzerdaten", nutzerdaten)

    if(nutzerdaten):
        status_ai_message = check_nutzerData_Input_daten(nutzerdaten)

        print("status_ai_message", status_ai_message)

        return status_ai_message




def check_nutzerData_Input_daten(nutzerdaten:str):

    print("trigger in check_nutzerData_Input_daten")

    # Split the catched values into strings for a value check
    nutzerdaten_liste = nutzerdaten.split()
    
    # get the keys that does not match the values: 
    nutzerdaten_kein_match = [key for key, value in patientenDaten.items() if value not in nutzerdaten_liste]


    # Adds the correct pronoun before the key for proper grammar
    pronouns = {
    "Name": "Ihren",
    "Geburtstag": "Ihren",
    "Nummer": "Ihre",
    "Dringlichkeit": "Ihren",
    "Untersuchung": "Ihre",
    "Tier": "Ihr",
    "Termin": "Ihre",
    }


    if len(nutzerdaten_kein_match) == 1:
        key = nutzerdaten_kein_match[0]
        pronoun = pronouns.get(key, "Ihren")
        return f"Ich habe gerade gesehen, dass unser System {pronoun} {key} nicht richtig übernommen hat. Können Sie mir bitte noch {pronoun} {key} nennen?"

    elif nutzerdaten_kein_match:
        fehlende = ", ".join(nutzerdaten_kein_match)
        return f"Leider fehlen noch folgende Daten: {fehlende}. Können Sie mir diese bitte nennen?"

    else:
        print("triggerd in db ")
        create_db_record(patientenDaten)
        return "Alle Daten sind vorhanden, danke!"




def create_db_record(): 
    print("data send to db", )


     


