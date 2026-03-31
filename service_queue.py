
class Request:
    """Represents the service that is request from the system.
    Will be used in our heap class as request objects
    
    """
    
    def __init__(self, id, name, room, priority, description=None ):
        self.id = id
        self.name = name
        self.room = room
        self.description = description
        self.priority = priority

class Maxheap:
    """Is a class that will store requets objects in the form of an array based max heap
    
    
    """
    def __init__(self):
        self.heap = []

    def getParentIndex(self, i):
        return(i-1)//2
    
    def getLeftChild(self, i):
        return i * 2+1
    
    def getRightChild(self, i):
        return i * 2+2
        


