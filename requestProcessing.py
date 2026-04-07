class Request:
    def __init__(self, request_id: int, request_type: str, details: str):
        self.request_id = request_id
        self.request_type = request_type  # "navigation" or "service"
        self.details = details

    def __str__(self):
        return f"[ID: {self.request_id}] Type: {self.request_type} | {self.details}"


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class RequestQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, request: Request):
        new_node = Node(request)
        if self.tail:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node
        self.size += 1

    def dequeue(self) -> Request:
        if self.is_empty():
            raise IndexError("Queue is empty")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return data

    def process_next(self) -> Request:
        if self.is_empty():
            raise IndexError("No requests to process")
        request = self.dequeue()
        print(f"  Processing {request}")
        return request

    def peek(self) -> Request:
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.head.data

    def is_empty(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        return self.size


def simulate_pipeline():
    queue = RequestQueue()

    requests = [
        Request(1,  "navigation", "ICT -> Library"),
        Request(2,  "service",    "IT support - Room 204"),
        Request(3,  "navigation", "Gym -> Residence"),
        Request(4,  "service",    "Maintenance - ENG Block"),
        Request(5,  "navigation", "Library -> Science A"),
        Request(6,  "service",    "Help desk - Student Union"),
        Request(7,  "navigation", "Parkade -> MFH"),
        Request(8,  "service",    "IT support - ICT Lab"),
        Request(9,  "navigation", "Residence -> Food Court"),
        Request(10, "service",    "Maintenance - Gym"),
        Request(11, "navigation", "Admin -> Health Centre"),
        Request(12, "service",    "Help desk - Library"),
        Request(13, "navigation", "Science A -> Parkade"),
        Request(14, "service",    "IT support - Arts Block"),
        Request(15, "navigation", "MFH -> Student Union"),
        Request(16, "service",    "Maintenance - Residence"),
        Request(17, "navigation", "Bus Stop -> ICT"),
        Request(18, "service",    "Help desk - Bookstore"),
        Request(19, "navigation", "ENG Block -> Gym"),
        Request(20, "service",    "IT support - Admin"),
    ]

    print("=== Enqueueing Requests ===")
    for r in requests:
        queue.enqueue(r)
        print(f"  Enqueued {r}")

    print(f"\nQueue size: {len(queue)}")
    print(f"Next to process: {queue.peek()}")

    print("\n=== Processing in Arrival Order ===")
    processed = 0
    while not queue.is_empty():
        queue.process_next()
        processed += 1

    print(f"\nDone. Total processed: {processed}")
    print(f"Queue empty: {queue.is_empty()}")


if __name__ == "__main__":
    simulate_pipeline()