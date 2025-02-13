"""
Google Calendar Automation Script

This script demonstrates how to authenticate with Google Calendar API,
create, update, and delete events using the Google Calendar service.

Author: W.Z
Date: 2024-12-28
"""
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import pdb
from tabulate import tabulate

# Scopes define the access your application needs
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """
    Authenticates with Google Calendar API.

    Returns:
        service: The authenticated Google Calendar service.
    """
    creds = None
    # Token file to store user's access and refresh tokens
    token_file = 'token.pickle'

    # Check if token file exists
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    # Build the service
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_user_input():
    """
    Get event details from user input.
    
    This function prompts the user to enter various details for an event, such as the event title, date and time, duration,
    location, description, and attendees. It then returns a dictionary containing all the entered details.
    
    Returns:
        dict: A dictionary containing the event details entered by the user.
    """
    summary = input("Enter event title: ")
    
    # Get today's date and show it as default
    today = date.today()
    date_str = input(f"Enter date (YYYY-MM-DD) [default: {today}]: ") or str(today)
    time_str = input("Enter start time (HH:MM): ")
    
    # Combine date and time
    start_time_str = f"{date_str} {time_str}"
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    
    # Get duration
    duration = int(input("Enter duration in minutes (default: 60): ") or "60")
    
    # Optional inputs
    timezone = input("Enter timezone (optional, press Enter to skip, default: Europe/London): ").strip() or "Europe/London"
    location = input("Enter location (optional, press Enter to skip): ").strip() or None
    description = input("Enter description (optional, press Enter to skip): ").strip() or None

    # Add color selection
    print("\nAvailable colors:")
    print("1: Lavender   2: Sage      3: Grape")
    print("4: Flamingo   5: Banana    6: Tangerine")
    print("7: Peacock    8: Graphite  9: Blueberry")
    print("10: Basil     11: Tomato")
    color_id = input("Enter color number (1-11, press Enter to skip): ").strip() or None
    
    # Get attendees
    attendees_str = input("Enter attendee emails (comma-separated, press Enter to skip): ").strip()
    attendees = [email.strip() for email in attendees_str.split(",")] if attendees_str else None
    
    return {
        "summary": summary,
        "start_time": start_time,
        "duration_minutes": duration,
        "timezone": timezone,
        "location": location,
        "description": description,
        "color_id": color_id,
        "attendees": attendees
    }

def create_event(service):
    """
    Creates a new event in Google Calendar.

    Args:
        service: The authenticated Google Calendar service.
    """
    try:
        event_details = get_user_input()
        event = {
            'summary': event_details['summary'],
            'start': {
                'dateTime': event_details['start_time'].isoformat(),
                'timeZone': event_details['timezone'],
            },
            'end': {
                'dateTime': (event_details['start_time'] + timedelta(minutes=event_details['duration_minutes'])).isoformat(),
                'timeZone': event_details['timezone'],
            },
            'location': event_details['location'],
            'description': event_details['description'],
            'colorId': event_details['color_id'],
            'attendees': [{'email': email} for email in event_details['attendees']] if event_details['attendees'] else [],
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Error creating event: {str(e)}")

def get_date_range() -> tuple[datetime, datetime, str]:
    """Get start and end dates from user input with default options."""
    today = date.today()
    
    print("\nEnter date range for events:")
    start_str = input(f"Start date (YYYY-MM-DD) [default: {today}]: ") or str(today)
    end_str = input(f"End date (YYYY-MM-DD) [default: {today + timedelta(days=7)}]: ") or str(today + timedelta(days=7))
    timezone = input("Enter timezone (optional, press Enter to skip, default: Europe/London): ").strip() or "Europe/London"
    
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d") + timedelta(days=1)  # Include the entire end date
        return start_date, end_date, timezone
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None, None, None

def list_events(service):
    """
    Lists events from start date to end date in Google Calendar.

    Args:
        service: The authenticated Google Calendar service.
    """
    start_date, end_date, timezone = get_date_range()
    tz = ZoneInfo(timezone)
    start_date = start_date.replace(tzinfo=tz)
    end_date = end_date.replace(tzinfo=tz)
    if not start_date or not end_date:
        return

    events_result = service.events().list(calendarId='primary', timeMin=start_date.isoformat(), timeMax=end_date.isoformat(), singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print("No events found.")
        return
    
    # Print events
    table_data = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        if 'T' in start:
            start_dt = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end_dt = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            start_str = start_dt.strftime("%Y-%m-%d %H:%M")
            end_str = end_dt.strftime("%Y-%m-%d %H:%M")
            time_str = f"{start_str} - {end_str}"
        else:
            time_str = f"{start} - {end}"        
        table_data.append([event['summary'], time_str, event.get('location', '')])
    # Print table using tabulate
    headers = ["Title", "Date/Time", "Location"]
    print("\nEvents List:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def update_event(service, event_id):
    """
    Updates an existing event in Google Calendar.

    Args:
        service: The authenticated Google Calendar service.
        event_id: The ID of the event to be updated.
    """
    # Implementation details...

def delete_event(service, event_id):
    """
    Deletes an event from Google Calendar.

    Args:
        service: The authenticated Google Calendar service.
        event_id: The ID of the event to be deleted.
    """
    # Implementation details...

def main():
    print("Google Calendar Automation Script")

    service = authenticate_google_calendar()
    while True:
        try:
            print("Select an option:")
            print("0. Exit")
            print("1. Create Event")
            print("2. List Events")
            choice = int(input("Enter your choice (0/1/2): "))
            if choice == 0:
                print("Exiting. Goodbye!")
                break
            elif choice == 1:
                create_event(service)
            elif choice == 2:
                list_events(service)
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please enter a number (0. Exit, 1. Create Event, 2. List Events).")


if __name__ == '__main__':
    main()

    # # Get the event ID (replace with the actual event ID you created or retrieved)
    # event_id = 'your-event-id'

    # # Update the event
    # update_event(service, event_id)

    # # Delete the event
    # delete_event(service, event_id)
