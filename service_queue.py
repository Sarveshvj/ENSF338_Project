
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
    
    def swap(self, i ,j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, request):
        self.heap.append(request)
        heap = self.heap
        i = len(heap)-1
        while i>0:
            parent = self.getParentIndex(i)
            if heap[i].priority > heap[parent].priority:
                self.swap(i,parent)
                i=parent


    def getMaxPriority(self):
        heap = self.heap
        result = heap[0]
        length = len(heap)-1
        heap[0], heap[length] = heap[length], heap[0]
        heap.pop(length)
        key = 0
        while key<= (len(heap)-1):
            if key*2+2 < len(heap) and heap[key].priority<heap[key*2+2].priority:
                heap[key], heap[key*2+2] = heap[key*2+2], heap[key]
                key = key*2+2
                continue
            elif key*2+1 < len(heap) and heap[key].priority<heap[key*2+1].priority  :
                heap[key], heap[key*2+1] = heap[key*2+1], heap[key]
                key = key*2+1
                continue
            break
        return result




        

        

    


        


