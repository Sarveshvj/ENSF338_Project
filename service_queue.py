class Request:
    def __init__(self, id, name, room, priority, description=None ):
        self.id = id
        self.name = name
        self.room = room
        self.description = description
        self.priority = priority

