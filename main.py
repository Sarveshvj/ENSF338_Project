from service_queue import Maxheap, Request




def add_request(heap):
    name = input("Enter requester name: ")
    room = input("Enter room ID: ")
    print("Priority levels: 1 = Low, 2 = Standard, 3 = Emergency")
    priority = int(input("Enter priority level (1-3): "))
    description = input("Enter description (or press Enter to skip): ")
    
    request = Request(Request._id_counter + 1, name, room, priority, description)
    heap.insert(request)
    print(f"\nRequest #{request.id} added successfully!")
