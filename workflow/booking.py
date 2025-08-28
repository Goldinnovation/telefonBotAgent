from datetime import datetime
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

from db.dbService import CreateEntryService


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
def check_current_date(context: RunContext):
    from datetime import datetime, timedelta
    import random
    
    def is_weekday(date):
        """Check if date is a weekday (Monday-Friday)"""
        return date.weekday() < 5  # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
    
    def get_next_working_days(start_date, count=5):
        """Get the next N working days starting from start_date"""
        working_days = []
        current_date = start_date
        
        while len(working_days) < count:
            if is_weekday(current_date):
                working_days.append(current_date)
            current_date += timedelta(days=1)
        
        return working_days
    
    # Get today's date
    today = datetime.now().date()
    
    # Get next 5 working days
    next_working_days = get_next_working_days(today, 5)
    
    # Create the dictionary with German day names
    day_names = {
        0: "Montag",
        1: "Dienstag", 
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag"
    }
    
    result = {}
    for i, date in enumerate(next_working_days):
        # Pick a random hour between 8 and 18 (8 AM to 6 PM)
        random_hour = random.randint(8, 18)
        
        # Create datetime object with random hour, minute=0, second=0, microsecond=0
        datetime_obj = datetime.combine(date, datetime.min.time().replace(hour=random_hour))
        
        if i == 0:
            result["Heute"] = datetime_obj.isoformat()
        else:
            day_name = day_names[date.weekday()]
            result[day_name] = datetime_obj.isoformat()
    
    return result



@function_tool
async def checks_users_totalInput_before_DBCreation(context: RunContext, nutzerdaten: str):

    """
    Checks which patient data fields are missing and returns appropriate messages.
    If all data is present, creates a DB record.
    """

    print("checks_users_totalInput_before_DBCreation is executed")
    print("Nutzerdaten", nutzerdaten)

    if(nutzerdaten):
        status_ai_message = await check_nutzerData_Input_daten(nutzerdaten)

        print("status_ai_message", status_ai_message)

        return status_ai_message




async def check_nutzerData_Input_daten(nutzerdaten:str):

    print("trigger in check_nutzerData_Input_daten")

    # Parse the incoming data and update patientenDaten
    try:
        import json
        new_data = json.loads(nutzerdaten)
        
        # Update the global patientenDaten with new data
        for key, value in new_data.items():
            if key in patientenDaten:
                patientenDaten[key] = value
                
        print("Updated patientenDaten:", patientenDaten)
        
    except Exception as e:
        print(f"Error parsing nutzerdaten: {e}")

    # Check which fields are missing from patientenDaten
    missing_fields = []
    for key, value in patientenDaten.items():
        if not value or value == "":
            missing_fields.append(key)

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

    print("missing_fields", missing_fields)
    if len(missing_fields) == 1:
        key = missing_fields[0]
        pronoun = pronouns.get(key, "Ihren")
        return f"Ich habe gerade gesehen, dass unser System {pronoun} {key} nicht richtig übernommen hat. Können Sie mir bitte noch {pronoun} {key} nennen?"

    elif missing_fields:
        fehlende = ", ".join(missing_fields)
        return f"Leider fehlen noch folgende Daten: {fehlende}. Können Sie mir diese bitte nennen?"

    else:
        print("triggerd in db ")

        # Create a PatientData object from the dictionary
        from db.dbSchema import PatientData
        patient = PatientData(**patientenDaten)
        await CreateEntryService(patient)
        
        return "Alle Daten sind vorhanden, danke!"



     


