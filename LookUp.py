class Room:
    def __init__(self, room_id, capacity, room_type):
        self.room_id = room_id
        self.capacity = capacity
        self.room_type = room_type
        self.bookings = []

    def __str__(self):
        return self.room_id


class Building:
    def __init__(self, building_id, name, location):
        self.building_id = building_id
        self.name = name
        self.location = location
        self.rooms = {}

    def add_room(self, room):
        self.rooms[room.room_id] = room

    def get_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        else:
            return None

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]

    def __str__(self):
        return self.building_id


class LookupSystem:
    def __init__(self, campus=None):
        self.buildings = {}
        self.rooms = {}
        self.campus = campus

    def add_building(self, building):
        self.buildings[building.building_id] = building

        if self.campus != None:
            alreadyThere = False
            for x in self.campus.buildings:
                if x.building_id == building.building_id:
                    alreadyThere = True
            if alreadyThere == False:
                self.campus.addBuilding(building.building_id)

    def get_building(self, building_id):
        if building_id in self.buildings:
            return self.buildings[building_id]

        if self.campus != None:
            for x in self.campus.buildings:
                if x.building_id == building_id:
                    return x

        return None

    def remove_building(self, building_id):
        if building_id in self.buildings:
            b = self.buildings[building_id]

            for r in list(b.rooms.keys()):
                if r in self.rooms:
                    del self.rooms[r]

            del self.buildings[building_id]

        if self.campus != None:
            target = None
            for x in self.campus.buildings:
                if x.building_id == building_id:
                    target = x
                    break

            if target != None:
                for r in list(target.rooms.keys()):
                    if r in self.rooms:
                        del self.rooms[r]
                del self.campus.buildings[target]

    def add_room(self, building_id, room):
        b = self.get_building(building_id)

        if b == None:
            print("building not found")
            return

        b.add_room(room)
        self.rooms[room.room_id] = room

    def get_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]

        for b in self.buildings:
            if room_id in self.buildings[b].rooms:
                return self.buildings[b].rooms[room_id]

        if self.campus != None:
            for x in self.campus.buildings:
                if room_id in x.rooms:
                    return x.rooms[room_id]

        return None

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]

        removed = False

        for b in self.buildings:
            if room_id in self.buildings[b].rooms:
                self.buildings[b].remove_room(room_id)
                removed = True
                break

        if removed == False and self.campus != None:
            for x in self.campus.buildings:
                if room_id in x.rooms:
                    del x.rooms[room_id]
                    break

    def print_all(self):
        print("Buildings:")
        for b in self.buildings:
            print(b)

        print("Rooms:")
        for r in self.rooms:
            print(r)


def main():
    from campusmap_pathnav import Campus
    import time

    campus = Campus()
    lookup = LookupSystem(campus)

    b1 = Building("ICT", "ICT Building", (0, 0))
    b2 = Building("ENG", "Engineering", (1, 1))

    lookup.add_building(b1)
    lookup.add_building(b2)

    room1 = Room("ICT-121", 100, "lecture")
    room2 = Room("ENG-201", 50, "lab")

    lookup.add_room("ICT", room1)
    lookup.add_room("ENG", room2)

    print("Building ICT:", lookup.get_building("ICT"))
    print("Room ICT-121:", lookup.get_room("ICT-121"))

    print("Missing building:", lookup.get_building("SCI"))
    print("Missing room:", lookup.get_room("XXX"))

    lookup.remove_room("ICT-121")
    print("After removing ICT-121:", lookup.get_room("ICT-121"))

    lookup.remove_building("ENG")
    print("After removing ENG:", lookup.get_building("ENG"))

    lookup.print_all()

    t1 = time.time()
    lookup.get_building("ICT")
    t2 = time.time()
    print("small lookup time:", t2 - t1)

    i = 0
    while i < 1000:
        temp = Building("B" + str(i), "Building" + str(i), (i, i))
        lookup.add_building(temp)
        i += 1

    t3 = time.time()
    lookup.get_building("B999")
    t4 = time.time()
    print("large lookup time:", t4 - t3)


if __name__ == "__main__":
    main()