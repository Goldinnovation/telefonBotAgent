
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


@function_tool
def set_user_profile_info(field: str):
    async def set_birtday_date(conext: RunContext, value: str):
        print(f'called birtday is {value}')
        return f'the field{field} was set to {value}'

    return set_birtday_date
   




# Gets the users birtdhay
@function_tool
def set_user_booking_type(field: str):
    async def set_type_appointment(context: RunContext, value: str):
        print(f'Art des Termin und für wen  {value}')
        return f'the field{field} was set to {value}'

    return set_type_appointment
   

# Gets the type of appointment 
@function_tool
def set_user_booking_type(field: str):
    print("tiggerd")
    async def set_type_appointment(context: RunContext, value: str):
        print(f'Art des Termin und für wen  {value}')
        return f'the field{field} was set to {value}'

    return set_type_appointment