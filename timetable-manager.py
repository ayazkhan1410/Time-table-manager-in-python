def main(): # main method

    timetable = [[] for _ in range(7)] # We create an empty timetable for seven days to organize events for each day of the week
    
    start_day = 0  # Set the start day of the week to Monday
    print("Weekly Timetable Manager") #  Printing a welcome message
    print("Author: Ayaz Khan") # Display the name of the author
    print("Email: programmingwithayaz\n") # Display the author's email addres

    while True:
        print_menu() # here we're printing the main menu of our program
        choice = input("Choose an option: ").strip() # here we take input from the user like what he/she wanted to do and we use .strip() method to remove the extra spaces 

        '''
        here we display the functions accoring to the user choice and in case of error we'll display the error message Invalid Input. Please choose again
        '''
        
        if choice == "1":
            create_event(timetable)
        elif choice == "2":
            update_event(timetable)
        elif choice == "3":
            delete_event(timetable)
        elif choice == "4":
            print_weekly_timetable(timetable, start_day)
        elif choice == "5":
            print_day_timetable(timetable)
        elif choice == "6":
            save_timetable(timetable)
        elif choice == "7":
            timetable = load_timetable()
        elif choice == "8":
            start_day = choose_start_day()
        elif choice == "9":
            search_events(timetable)
        elif choice == "0":
            print("Exiting the program. Goodbye!")
            return
        else:
            print("Invalid Input. Please choose again.")

def print_menu():
    """
   This function will going to print the whole menu
    
    """
    print("\nMenu:")
    print("1. Create an event")
    print("2. Update an event")
    print("3. Delete an event")
    print("4. Print the weekly timetable")
    print("5. Print the timetable for a specific day")
    print("6. Save the timetable to a file")
    print("7. Load the timetable from a file")
    print("8. Choose start day of the week")
    print("9. Search for events")
    print("0. Quit")
    
def create_event(timetable):
    
    """
    In this function we will going to enable the user to add a new event to the weekly timetable. This function will Take the user input such as the event title, start time, end.
    """
    
    day = get_day()
    title, start_time, end_time, location = get_event_details()

    start_time_valid = is_time_valid(start_time)
    end_time_valid = is_time_valid(end_time)
    order_valid = is_time_order_valid(start_time, end_time)

    if not start_time_valid or not end_time_valid or not order_valid:
        print("Invalid time. Please make sure start time is before end time and in HH:MM format like (18:00) - (20:00)")
        return

    time_available = is_time_available(timetable[day], start_time, end_time)
    if not time_available:
        print("Time slot not available. Event overlaps with another event.")
        return

    event = {"title": title, "start": start_time, "end": end_time, "location": location}
    timetable[day].append(event)
    timetable[day].sort(key=lambda e: e["start"])
    
    print('-----------------------------------')
    print("Event added successfully.")
    print('-----------------------------------')

def update_event(timetable):
    
    """
   well this function is used to update the event it first takes the input from the user like which scheduled event he/she wants to update and then checks if the event exists in our timetable in this case it will take the updated event title and reschedule the time of the event and update the event in the timetable or in case of any error it will print error message such as No event found with this search term OR Multiple events found. 
    """
    
    day = get_day()
    search_term = input("Enter an event name to search for the event to update: ").strip()
    events = [event for event in timetable[day] if search_term.lower().strip() == event["title"].lower().strip()]

    if not events:
        print("No event found")
        return

    if len(events) > 1:
        print("Multiple events found.")
        return
    
    event = events[0]
    title, new_start_time, new_end_time, location = get_event_details()
    
    if not is_time_valid(new_start_time) or not is_time_valid(new_end_time) or not is_time_order_valid(new_start_time, new_end_time):
        print("Invalid time. Please ensure start time is before end time and in HH:MM format.")
        return
    
    timetable[day].remove(event)
    
    if not is_time_available(timetable[day], new_start_time, new_end_time):
        print("Sorry, that time slot is already taken. It clashes with another event.")
        timetable[day].append(event)  
        return
    
    event.update({"title": title, "start": new_start_time, "end": new_end_time, "location": location})
    timetable[day].append(event)
    timetable[day].sort(key=lambda e: e["start"])
    
    print('-----------------------------------')
    print("Event updated successfully.")
    print('-----------------------------------')

def delete_event(timetable):
    
    """
    this function first take the input from the user like which event he/she wants to search then if the event found it will display the event with the name of the day and in case of error it will display error messages like No event found OR Multiple events found.
    """
    
    day = get_day()
    search_term = input("Enter a keyword to search for the event to delete: ").strip().lower()  
    events = [event for event in timetable[day] if search_term == event["title"].lower()] 
    
    if not events:
        print("No event found")
        return

    if len(events) > 1:
        print("Multiple events found")
        return
    
    event = events[0]
    timetable[day].remove(event)
    
    print('-----------------------------------')
    print("Event deleted successfully.")
    print('-----------------------------------')

def print_weekly_timetable(timetable, start_day):
    
    """
    this function will print the whole week and in case if we didn't schedule any event it will print No events scheduled.
    """
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days = days[start_day:] + days[:start_day] 
    for i, day in enumerate(days):
        day_index = (start_day + i) % 7
        print(f"{day}:")
        if timetable[day_index]:
            for event in timetable[day_index]:
                print_event(event)
        else:
            print('-----------------------------------')
            print("No events scheduled.")
            print('-----------------------------------')

def print_day_timetable(timetable):
    
    """
    This function is somewhat similar to our above function because it will also print the schedule but for a specific day and same in case of no schedule it will print No events scheduled for this day.
    """
    day = get_day()
    if timetable[day]:
        for event in timetable[day]:
            print_event(event)
    else:
        print('-----------------------------------')
        print("No events scheduled for this day.")
        print('-----------------------------------')

def save_timetable(timetable):
    
    """
   this function is used to save the timetable which we previously input from the user what this function will going to do first it take the filename as input from the user after that it saves the timetable within a current directory and in case of any error it will display error message like An error occurred while saving the timetable, Please try again.
    """
    
    filename = input("Enter the filename to save the timetable: ").strip()
    try:
        
        with open(filename, "w") as file:
            for day in timetable:
                for event in day:
                    if event["location"]:
                        location = event["location"]
                    else:
                        location = "N/A"
                    file.write(f"{event['title']},{event['start']},{event['end']},{location}\n")
                    
        print('-----------------------------------')
        print("Timetable saved successfully.")
        print('-----------------------------------')
    except IOError:
        print("An error occurred while saving the timetable, Please try again ")


def load_timetable():
    
    """
   this function will load the saved timetable. First, it will take the filename as input from the user like which file he/she wants to load if the file exists then in this case it will load the saved timetable and if the file does exist then in this case it will throw an error message which will File not found OR An error occurred while loading the timetable. Please try again.
    """
    
    filename = input("Enter the filename to load the timetable: ").strip()
    new_timetable = [[] for _ in range(7)]

    try:
        with open(filename, "r") as file:
            for line in file:
                title, start_time, end_time, location = line.strip().split(",")
                location = location if location != "N/A" else ""
                day_index = get_day_from_time(start_time)
                event = {"title": title, "start": start_time, "end": end_time, "location": location}
                new_timetable[day_index].append(event)

        for day_events in new_timetable:
            day_events.sort(key=lambda e: e["start"])
            
        print('-----------------------------------')
        print("Timetable loaded successfully.")
        print('-----------------------------------')
        return new_timetable
    except FileNotFoundError:
        print("File not found")
        return [[] for _ in range(7)]
    except IOError:
        print("An error occurred while loading the timetable. Please try again.")
        return [[] for _ in range(7)]
    except ValueError:
        print("File format error. Please check the file content and try again.")
        return [[] for _ in range(7)]


def choose_start_day():
    
    """
    This function will iteratively requests the user to input a number representing the start day of the week where 0 represent to Monday, 1 to Tuesday ..... and 6 to sunday.
    """
    
    while True:
        try:
            start_day = int(input("Enter the start day of the week (0=Monday, 6=Sunday): ").strip())
            if 0 <= start_day <= 6:
                return start_day
            else:
                print("Invalid day. Please enter a number between 0 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 6.")

def search_events_in_day(events, keyword):
    
    """
    This function will going to searches for events containing a specific keyword within their title or location. It returns a list of matching events.
    """
    matches = []
    keyword = keyword.lower().strip()
    for event in events:
        event_title = event["title"].lower().strip()
        event_location = event["location"].lower().strip() if event["location"] else ""
        if keyword in event_title or keyword in event_location:
            matches.append(event)
    return matches

def print_event(event):
    
    """
    This function will going to  prints the details of an event including its title, start time, end time, and location. 
    """
    
    if event["location"]:
        location = event["location"]
    else:
        location = "N/A"
    print(f"  {event['start']} - {event['end']}: {event['title']} at {location}")

def search_events(timetable):
    
    """
   This function searches for events in the weekly timetable based on a user-provided keyword and displays the results.
    """
    
    keyword = input("Enter a keyword to search for events: ").strip().lower()
    matches = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for day in range(7):
        day_matches = search_events_in_day(timetable[day], keyword)
        for event in day_matches:
            matches.append((days[day], event))

    if matches:
        for day, event in matches:
            print(f"{day}: ", end="")
            print_event(event)
    else:
        print("No events found matching the keyword.")

def get_day():
    
    """
    This function will continuously ask the user to input a number corresponding to a day of the week, where 0 represent to Monday, 1 to Tuesday ..... and 6 to sunday.
    """
   
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    while True:
        try:
            day = int(input("Enter the day of the week (0=Monday, 6=Sunday): ").strip())
            if 0 <= day <= 6:
                return day
            else:
                print("Invalid day. Please enter a number between 0 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 6.")

def get_event_details():
    
    """
    this function will going to display the detail of the event which we previously scheduled
    """
    
    title = input("Enter the event title: ").strip()
    start_time = input("Enter the start time (HH:MM): ").strip()
    end_time = input("Enter the end time (HH:MM): ").strip()
    location = input("Enter the event location (optional): ").strip()
    return title, start_time, end_time, location

def is_time_valid(time_str):
    
    '''
    This function will going to checks if a given time input is valid, and it also make sure that the format must be in (HH:MM) form and falls within the valid range of hours (0-23) and minutes (0-59).
    '''
    
    parts = time_str.split(":")
    if len(parts) != 2:
        return False

    hour_str, minute_str = parts
    if not hour_str.isdigit() or not minute_str.isdigit():
        return False

    hour, minute = int(hour_str), int(minute_str)
    return 0 <= hour < 24 and 0 <= minute < 60

def is_time_order_valid(start_time, end_time):
    
    """
    This function will going to checks if the start time of an event is before its end time. It returns True if the start time is before the end time and False otherwise.
    """
    
    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))
    return (start_hour < end_hour) or (start_hour == end_hour and start_minute < end_minute)

def is_time_available(events, start_time, end_time):
    
    '''
    This function will going to checks if a given time slot is available in a list of events. It returns True if the time slot is available and False otherwise.
    '''
    for event in events:
        if not (end_time <= event["start"] or start_time >= event["end"]):
            return False
    return True

def print_event(event):
    
    '''
    This function will going to prints the details of an event, including its start and end times, title, and location if available. If the location is not Available, it prints "N/A" instead.

    '''
    
    location = event["location"]
    if location:
        print(f"  {event['start']} - {event['end']}: {event['title']} at {location}")
    else:
        print(f"  {event['start']} - {event['end']}: {event['title']} at N/A")


def get_day_from_time(time_str):
    
    """
    This function will going to extracts the day of the week from a given time Input. If the time string is in the correct format (HH:MM), it returns the corresponding day of the week (0 for Monday, 1 for Tuesday, ..., 6 for Sunday). If the format is incorrect or the time is invalid, it returns 0.
    """
    
    parts = time_str.split(":")
    if len(parts) != 2:
        return 0
    
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        if 0 <= hour < 24 and 0 <= minute < 60:
            return (hour // 24) % 7
        else:
            return 0
    except ValueError:
        return 0

if __name__ == "__main__":
    """
    This function starts the program. It checks if the script is being run directly, and if it is, it runs the main function.
    """
    main()
