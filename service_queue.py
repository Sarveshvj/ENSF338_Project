
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


