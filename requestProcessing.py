class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class RequestQueue:
    def __init__(self):
        self.head = None  # front of queue (dequeue from here)
        self.tail = None  # back of queue (enqueue here)
        self.size = 0

    def enqueue(self, request):
        new_node = Node(request)
        if self.tail:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.head.data

    def is_empty(self):
        return self.head is None

    def __len__(self):
        return self.size