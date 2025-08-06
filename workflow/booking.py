
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
    "name": "",
    "geburtstag":"", 
    "nummer":"", 
    "status":"",
    "untersuchungsart":"", 
    "tier": "",
    "Zeit": ""

}

@function_tool
def set_user_profile_info(field: str):
    async def set_birtday_date(conext: RunContext, value: str):
        print(f'called birtday is {value}')
        return f'the field{field} was set to {value}'

    return set_birtday_date
   






# Gets the type of appointment 
@function_tool
async def set_type_appointment(context: RunContext, untersuchungsart: str, tier:str):
    print(f'Art des Termin und für wen  {untersuchungsart}')
    print(f'tier des patienten  {tier}')


    patientenDaten["untersuchungsart"] = untersuchungsart
    patientenDaten["tier"] = tier

    return f'wurde erfolgreich eingetragen'

    return set_type_appointment



@function_tool
async def set_user_info(context: RunContext, name: str, geburtstag: str, nummer: str ):
    print(f'name: {name}')
    print(f'geburtstag: {geburtstag}')
    print(f'numner {nummer}')

    patientenDaten["name"] = name
    patientenDaten["geburtstag"] = geburtstag
    patientenDaten["nummer"] = nummer



    return f'Super sie sind jetzt im system.'



@function_tool
async def set_user_booking_petStatus_and_time(context: RunContext, DringlichkeitStatus: str, Datum:str, Zeit:str):
    print(f'DringlichkeitStatus {DringlichkeitStatus}')
    print(f'Zeit {Zeit}')

    patientenDaten["status"] = DringlichkeitStatus
    patientenDaten["Zeit"] = Zeit
  


    return f'Super ich hab information eingetragen sind jetzt im system.'

     



@function_tool
async def send_user_data_to_DB(context: RunContext, value:str):

    print("patienten daten am Ende", patientenDaten)
    print("value", value)
  


    return f'Daten wurden erfolgreich hinterlegt'

     


