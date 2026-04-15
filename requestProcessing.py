class Request:
    """
    Represents a single incoming request in the campus system.
    Each request has a unique ID, a type (navigation or service),
    and a details string describing what is being requested.
    """

    def __init__(self, request_id: int, request_type: str, details: str):
        """
        Initialize a Request object.
        Args:
            request_id: Unique identifier for the request.
            request_type: Type of request — 'navigation' or 'service'.
            details: Description of the request.
        """
        self.request_id = request_id
        self.request_type = request_type
        self.details = details

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the request.
        """
        return f"[ID: {self.request_id}] Type: {self.request_type} | {self.details}"


class Node:
    """
    A single node in the linked list used by RequestQueue.
    Holds a Request object and a pointer to the next node.
    """
    def __init__(self, data: Request):
        """
        Initialize a Node with data and no next pointer.
        Args:
            data: The Request object stored in this node.
        """
        self.data = data
        self.next = None


class RequestQueue:
    """
    A FIFO queue implemented using a singly linked list.
    Incoming requests are enqueued at the tail and dequeued from
    the head, preserving strict arrival order at all times.
    Both enqueue and dequeue run in O(1) time.
    """

    def __init__(self):
        """
        Initialize an empty RequestQueue with head, tail, and size.
        """
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, request: Request) -> None:
        """
        Add a new request to the tail of the queue.
        Args:
            request: The Request object to add.
        """
        new_node = Node(request)
        if self.tail:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node
        self.size += 1

    def dequeue(self) -> Request:
        """
        Remove and return the request at the head of the queue.

        Returns:
            The Request object at the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return data

    def process_next(self) -> Request:
        """
        Dequeue and process the next request in arrival order.

        Returns:
            The processed Request object.

        Raises:
            IndexError: If there are no requests to process.
        """
        if self.is_empty():
            raise IndexError("No requests to process")
        request = self.dequeue()
        print(f"  Processing {request}")
        return request

    def peek(self) -> Request:
        """
        Return the front request without removing it.

        Returns:
            The Request object at the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.head.data

    def is_empty(self) -> bool:
        """
        Check whether the queue has no requests.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return self.head is None

    def __len__(self) -> int:
        """
        Return the number of requests currently in the queue.
        """
        return self.size


def get_sample_requests() -> list:
    """
    Return a hardcoded list of 20 sample requests for simulation.

    Includes a mix of navigation and service request types to
    demonstrate the pipeline handling both categories in arrival order.

    Returns:
        A list of 20 Request objects.
    """
    return [
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


def simulate_pipeline() -> None:
    """
    Simulate the incoming request processing pipeline.

    Enqueues 20 sample requests and processes them in arrival order,
    demonstrating correct FIFO behaviour of the RequestQueue.
    """
    queue = RequestQueue()

    # enqueue all sample requests
    print("=== Enqueueing Requests ===")
    for r in get_sample_requests():
        queue.enqueue(r)
        print(f"  Enqueued {r}")

    print(f"\nQueue size: {len(queue)}")
    print(f"Next to process: {queue.peek()}")

    # process all requests in arrival order
    print("\n=== Processing in Arrival Order ===")
    processed = 0
    while not queue.is_empty():
        queue.process_next()
        processed += 1

    print(f"\nDone. Total processed: {processed}")
    print(f"Queue empty: {queue.is_empty()}")


if __name__ == "__main__":
    simulate_pipeline()