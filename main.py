from service_queue import Maxheap, Request

from booking_system import BookingSystem



#-----------------------Service Queue-----------------------------------------------------------------
def add_request(heap):
    name = input("Enter requester name: ")
    room = input("Enter room name: ")
    print("Priority levels: 1 = Low, 2 = Standard, 3 = Emergency")
    priority = int(input("Enter priority level (1-3): "))
    description = input("Enter description or press Enter to skip: ")
    
    request = Request(Request._id_counter + 1, name, room, priority, description)
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