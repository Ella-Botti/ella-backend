import json
from datetime import date


def search_fact():
    with open('./json/calendar.json') as json_file:
        data = json.load(json_file)
        todays_date = date.today()
        events = []
        #compares all event dates and checks if the date matches with todays_date
        for key in data:
            if data[key]:
                month = data[str(key)]['kuukausi']
                day = data[str(key)]['paiva']
                #if the dates match, append to events that have happened today
                if month == str(todays_date.month) and day == str(todays_date.day):
                    event = f"Tänään {day}.{month}, vuonna {data[key]['vuosi']} {data[key]['tapahtuma']}"
                    events.append(event)
        print(events)
        return(events)