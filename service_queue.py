
class Request:
    """Represents the service that is request from the system.
    Will be used in our heap class as request objects
    
    """
    _id_Counter = 0

    def __init__(self, name, room, priority, description=None ):
        Request._id_Counter += 1
        self.id = Request._id_Counter
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
            else:
                break


    def getMaxPriority(self):
        
        heap = self.heap
        if not heap:
            return None
        
        result = heap[0]

        length = len(heap)-1
        
        self.swap(0,length)

        heap.pop(length)

        key = 0

        while key <= (len(heap)-1):
            right = self.getRightChild(key)
            left = self.getLeftChild(key)
            largest = key
            
            if left < len(heap) and heap[left].priority > heap[largest].priority:
                largest = left
            
            if right < len(heap) and heap[right].priority > heap[largest].priority:
                largest = right
            
            if largest != key:
                self.swap(key, largest)
                key = largest
            else:
                break
        return result




        

        

    


        


