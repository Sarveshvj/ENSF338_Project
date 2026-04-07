from service_queue import Maxheap, Request

from booking_system import BookingSystem



#-----------------------Service Queue-----------------------------------------------------------------
def add_request(heap):
    name = input("Enter requester name: ")
    room = input("Enter room name: ")
    print("Priority levels: 1 = Low, 2 = Standard, 3 = Emergency")
    priority = int(input("Enter priority level (1-3): "))
    description = input("Enter description or press Enter to skip: ")
    
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



def main():
    heap = Maxheap()
    system= BookingSystem()
    while True:
        print("          Campus Management        ")
        print("Campus Map and Shortest Path (1)")
        print("Route History and Undo (2)")
        print("Room and Event Booking (3)")
        print("Priority-Based Service Queue (4)")
        print("Fast Building and Resource Lookup (5)")
        print("Incoming Request Processing (6)")
        print(" Exit (0)")
        choice = input()


        if choice == "1":
            # 1 - Campus map and shortest path 
            pass

        elif choice == "2":
            # 2 - Navigation history and undo
            pass

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





