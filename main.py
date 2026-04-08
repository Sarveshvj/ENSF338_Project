from service_queue import Maxheap, Request

from booking_system import BookingSystem

from navigation_history import NavigationHistory

from campusmap_pathnav import Campus


#-----------------------Service Queue-----------------------------------------------------------------
def add_request(heap):
    name = input("Enter requester name: ")
    room = input("Enter room name: ")
    print("Priority levels: 1 = Low, 2 = Standard, 3 = Emergency")
    priority = int(input("Enter priority level (1-3): "))
    description = input("Enter description or press Enter to skip: ") or None
    
    request = Request(name, room, priority, description)
    heap.insert(request)
    print(f"\nRequest #{request.id} added successfully!")

def serve_request(heap):
    request = heap.getMaxPriority()
    if request is None:
        print("No requests in queue.")
        return
    print(f"\nServing Request #{request.id}")
    print(f" Name: {request.name}")
    print(f" Room: {request.room}")
    print(f" Priority: {request.priority}")
    print(f" Description: {request.description}")


def view_queue(heap):
    if not heap.heap:
        print("Queue is empty.")
        return
    print("\nCurrent Service Queue: ")
    for i in heap.heap:
        if i.description is not None:
            desc = f" - {i.description}"
        else:
            desc = ""
        print(f"\n Priority level: {i.priority} Request #{i.id} - {i.name} - {i.room}\n -{desc}")
#------------------------------End Of Service----------------------------------------------------
#----------------------------Booking system------------------------------------------------------



def add_booking(system):
    room_id = input("Enter room ID: ")
    date = input("Enter date in the format of YYYY-MM-DD: ")
    start_time = input("Enter start time in HH:MM format: ")
    end_time = input("Enter end time in HH:MM format: ")
    event_name = input("Enter event name: ")
    
    booking = system.add_booking(room_id, date, start_time, end_time, event_name)
    if booking:
        print(f"\nBooking #{booking.booking_id} added")

def remove_booking(system):
    booking_id = int(input("Enter booking ID to remove: "))
    system.remove_booking(booking_id)


def view_bookings_on_date(system):
    date = input("Enter date in the format of YYYY-MM-DD: ")
    bookings = system.get_bookings_on_date(date)
    if not bookings:
        print(f"No bookings found on that date: {date}")
        return
    print(f"\nThere are bookings on: {date}")
    for i in bookings:
        print(f" {i} ")


def view_bookings_in_range(system):
    start_date = input("Enter the start date in the format YYYY-MM-DD: ")
    start_time = input("Enter the start time HH:MM format: ")
    end_date = input("Enter the start date in the format YYYY-MM-DD: ")
    end_time = input("Enter the start time HH:MM format: ")
    bookings = system.get_bookings_in_range(start_date, start_time, end_date, end_time)
    if not bookings:
        print("No bookings found in that range.")
        return
    print(f"\n Bookings from {start_date} at {start_time} to {end_date} at {end_time}")
    for i in bookings:
        print(f" {i}")

def view_next_upcoming(system):
    date = input("Enter the start date in the format YYYY-MM-DD: ")
    time = input("Enter the start time HH:MM format: ")
    booking = system.next_upcoming(date, time)
    if booking:
        print(f"\n Upcoming: {booking}")
    else:
        print("No upcoming bookings found.")

#------------------------------End Of Booking System---------------------------------------------
#----------------------------Navigation History--------------------------------------------------
def view_current_location(nav_history):
    if nav_history.current_origin is None:
        print("\nNo current location")
    else:
        print(f"Current Location: {nav_history.current_origin}")

def view_history(nav_history):
    if nav_history.current_origin is None:
        print("\nNo current location")
    else:
        view_current_location(nav_history)
        print(f"\nUndo History: {nav_history.back_stack}")
        print(f"\nForward History: {nav_history.forward_stack}")

def undo_navigation(nav_history):
    nav_history.undo()
    print(f"\nYou are now at: {nav_history.current_origin}")

def forward_navigation(nav_history):
    nav_history.forward()
    print(f"\nYou are now at: {nav_history.current_origin}")

def navigate_to_location(nav_history, campus):
    origin_id = input("Enter origin building ID: ")
    dest_id = input("Enter destination building ID: ")
    
    origin_building = None
    dest_building = None
    
    for building in campus.buildings:
        if building.building_id == origin_id:
            origin_building = building
        if building.building_id == dest_id:
            dest_building = building
    
    if origin_building is None or dest_building is None:
        print("Invalid building ID(s)")
        return
    
    campus.displayShortestPath(origin_building, dest_building)

    nav_history.navigate(origin_id, dest_id)

    print(f"\nYou are now at: {dest_id}")
#----------------------------End of Navigation History-------------------------------------------


def main():
    heap = Maxheap()
    system= BookingSystem()
    nav_history = NavigationHistory()
    campus = Campus()
    campus.fileImport("test.dot")
    while True:
        print("\n========== Campus Management System ==========")
        print("1. Campus Map and Shortest Path")
        print("2. Route History and Undo")
        print("3. Room and Event Booking")
        print("4. Priority-Based Service Queue")
        print("5. Fast Building and Resource Lookup")
        print("6. Incoming Request Processing")
        print("0. Exit")
        print("==============================================")
        choice = input("\nEnter choice: ")

        if choice == "1":
            # 1 - Campus map and shortest path 
            pass

        elif choice == "2":
            print("\nRoute History and Navigation Undo")
            print("Navigate to Location (1)")
            print("Undo Last Navigation (2)")
            print("Go Forward (3)")
            print("View Current Location (4)")
            print("View History (5)")
            sub_choice = input("\nEnter choice: ")
            if sub_choice == "1":
                navigate_to_location(nav_history, campus)
            elif sub_choice == "2":
                undo_navigation(nav_history)
            elif sub_choice == "3":
                forward_navigation(nav_history)
            elif sub_choice == "4":
                view_current_location(nav_history)
            elif sub_choice == "5":
                view_history(nav_history)
            else:
                print("Invalid choice.")
        elif choice == "3":
            print("\nRoom and Event Booking ")
            print("Add Booking (1)")
            print("Remove Booking (2)")
            print("View Bookings on Date (3)")
            print("View Bookings in Range (4)")
            print("View Next Upcoming Booking (5)")
            sub_choice = input("\nEnter choice: ")
            if sub_choice == "1":
                add_booking(system)
            elif sub_choice == "2":
                remove_booking(system)
            elif sub_choice == "3":
                view_bookings_on_date(system)
            elif sub_choice == "4":
                view_bookings_in_range(system)
            elif sub_choice == "5":
                view_next_upcoming(system)
            else:
                print("Invalid choice.")

        elif choice == "4":
            print("\n Priority Service Queue ")
            print(" Add Request (1)")
            print(" Serve Next Request (2)")
            print(" View Queue (3)")
            sub_choice = input("\nEnter choice: ")
            if sub_choice == "1":
                add_request(heap)
            elif sub_choice == "2":
                serve_request(heap)
            elif sub_choice == "3":
                view_queue(heap)
            else:
                print("Invalid choice.")

        elif choice == "5":
            # 5 - Building and resource lookup 
            pass

        elif choice == "6":
            # 6 - Incoming request processing 
            pass

        elif choice == "0":
            print("Exiting")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

