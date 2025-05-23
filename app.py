import requests

BASE_URL = "http://localhost:5000/api/"

def display_events():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("EVENT PLANNER SYSTEM".center(50))
    print("=" * 50)
    print("1. Add Events ")
    print("2. Edit Events")
    print("3. Delete Events ")
    print("4. View Calendar")
    print("5. View all events")
    print("6. Search events ")
    print("7. Exit")
    print("=" * 50)

def add_events():
    """Add a new event """
    name = input("\nEnter event name: ")
    date = input("\nEnter event date (YYYY-MM-DD): ")
    location = input("\nEnter event location: ")
    reminder = input("\nEnter event reminder: ")
    reminder_time = input("\nEnter event reminder time/day: ")
    description = input("\nEnter event description: ")

    if not name:
        print("\nEvent name is required!")
        return

    event = {
        "name": name,
        "event_date": date,
        "location": location,
        "reminder": reminder.lower() == 'true',
        "reminder_time": reminder_time,
        "description": description if description else " "
    }
    
    try: 
        response = requests.post(f"{BASE_URL}/events", json=event)
        if response.status_code == 201:
            print("\nEvent added successfully!")
            new_event = response.json()
            print("\n" + "=" * 130)
            print(f"ID: {new_event['id']}, Name: {new_event['name']}, Date: {new_event['event_date']}, Location: {new_event['location']}, Reminder: {new_event['reminder']}, Reminder Time: {new_event['reminder_time']}, Description: {new_event['description']}")
            print("=" * 130)
        else:
            print(f"\nError adding event: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def edit_events():
    """Edit an existing event"""
    event_id = input("\nEnter event ID to edit: ")

    try:
        response = requests.get(f"{BASE_URL}/events/{event_id}")
        if response.status_code != 200:
            print(f"\nError: {response.text if response.status_code != 404 else 'Event not found!'}")
            return
        current_event = response.json()
        print("\nCurrent event details:")
        print(f"1. ID: {current_event['id']}")
        print(f"2. Name: {current_event['name']}")
        print(f"3. Date: {current_event['event_date']}")
        print(f"4. Location: {current_event['location']}")
        print(f"5. Reminder: {current_event['reminder']}")
        print(f"6. Reminder Time: {current_event['reminder_time']}")
        print(f"7. Description: {current_event.get('description', 'N/A')}")

        print("\nEnter new details (leave blank to keep current value):")
        updates = {}

        name = input("New name: ")
        if name:
            updates["name"] = name

        event_date = input("New event date (YYYY-MM-DD): ")
        if event_date:
            updates["event_date"] = event_date

        location = input("New location: ")
        if location:
            updates["location"] = location

        reminder = input("Set reminder: ")
        if reminder:
            updates["reminder"] = reminder.lower() == 'true'

        reminder_time = input("New reminder time: ")
        if reminder_time:
            try:
                updates["reminder_time"] = int(reminder_time)
            except ValueError:
                print("Reminder time must be a number!")
                return

        description = input("New description: ")
        if description:
            updates["description"] = description

        if not updates:
            print("\nNo changes made.")
            return

        try:
            updated_event = response.json()
            if 'id' in updated_event:
                print(f"ID: {updated_event['id']}, Name: {updated_event['name']}, Date: {updated_event['event_date']}, Location: {updated_event['location']}, Reminder: {updated_event['reminder']}, Reminder Time: {updated_event['reminder_time']}, Description: {updated_event['description']}")
            else:
                print("Response:", updated_event.get('message', 'Event updated.'))
        except ValueError:
                print("Event updated, but response could not be parsed as JSON.")

        try:
            response = requests.put(f"{BASE_URL}/events/{event_id}", json=updates)
            if response.status_code == 200:
                print("\n" + "-" * 50)
                print("\nEvent updated successfully!")
                print("-" * 50)
            else:
                print(f"\nError updating event: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\nConnection error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")



def delete_events():
    """Delete an existing event"""
    event_id = input ("\nEnter event ID to delete: ")
    confirm = input(f"\nAre you sure you want to delete event ID {event_id}? (y/n): ")

    if confirm.lower() != 'y':
        print("\n" + "-" * 50)
        print("\nEvent deletion cancelled.")
        print("-" * 50)
        return
    
    try:
        response = requests.delete(f"{BASE_URL}/events/{event_id}")
        if response.status_code == 200:
            print("\n" + "-" * 50)
            print("\nEvent deleted successfully!")
            print("-" * 50)
        else:
            print(f"\nError deleting event: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")        

def view_calendar():
    """View all events in the calendar"""
    try:
        response = requests.get(f"{BASE_URL}/events")
        if response.status_code == 200:
            events = response.json()
            if events:
                print("\n" + "-" * 50)
                print("EVENT CALENDAR".center(50))
                print("-" * 50)
                event_dates = [event['event_date'] for event in events]
                print("List of Event Dates:".center(50))
                print("-" * 50)
                for date in event_dates:
                    print(f"- {date}")
                print("-" * 50)
            else:
                print("\nNo events found.")
        else:
            print(f"\nError retrieving events: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def view_all_events():
    """View all events"""
    try:
        response = requests.get(f"{BASE_URL}/events")
        if response.status_code == 200:
            events = response.json()
            if events:
                print("\n" + "-" * 130)
                print("ALL EVENTS".center(50))
                print("-" * 130)
                print(f"{'ID':<5} {'Name':<20} {'Date':<40} {'Location':<20} {'Reminder':<10} {'Reminder Time':<15} {'Description':<20}")
                print("-" * 130)

                for event in events:
                    print(f"{event['id']:<5} {event['name']:<20} {event['event_date']:<40} {event['location']:<20} {event['reminder']:<10} {event['reminder_time']:<15} {event.get('description', 'N/A'):<20}")
                print("-" * 50)
            else:
                print("\nNo events found.")
        else:
            print(f"\nError retrieving events: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def search_events():
    """Search for an event by ID"""
    try:
        id_input = input("\nEnter event ID to search: ").strip()
        if not id_input.isdigit():
            print("\nInvalid ID. Please enter a numeric value.")
            return

        event_id = int(id_input)
        response = requests.get(f"{BASE_URL}/events/{event_id}")
        
        if response.status_code == 200:
            event = response.json()
            print("\n" + "-" * 50)
            print("EVENT DETAILS".center(50))
            print("-" * 50)
            print(f"ID: {event['id']}")
            print(f"Name: {event['name']}")
            print(f"Date: {event['event_date']}")
            print(f"Location: {event['location']}")
            print(f"Reminder: {event['reminder']}")
            print(f"Reminder Time: {event['reminder_time']}")
            print(f"Description: {event.get('description', 'N/A')}")
            print("-" * 50)
        elif response.status_code == 404:
            print("\nEvent not found.")
        else:
            print(f"\nError retrieving event: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def main():
    """Main function to run the program"""
    while True:
        display_events()
        choice = input("\nEnter your choice (1-7): ")

        if choice == '1':
            add_events()
        elif choice == '2':
            edit_events()
        elif choice == '3':
            delete_events()
        elif choice == '4':
            view_calendar()
        elif choice == '5':
            view_all_events()
        elif choice == '6':
            search_events()
        elif choice == '7':
            print("\nExiting the program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    main()