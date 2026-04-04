




# Important:
# - get_building() and get_room() return None if not found
# - remove_building() will also remove all rooms under that building





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
        self.rooms = {}   # room_id -> Room

    def add_room(self, room):
        self.rooms[room.room_id] = room

    def get_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        return None

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]

    def __str__(self):
        return self.building_id


class LookupSystem:
    def __init__(self):
        self.buildings = {}   # building_id -> Building
        self.rooms = {}       # room_id -> Room

    # ---------- building ----------
    def add_building(self, building):
        self.buildings[building.building_id] = building

    def get_building(self, building_id):
        if building_id in self.buildings:
            return self.buildings[building_id]
        return None

    def remove_building(self, building_id):
        if building_id in self.buildings:
            building = self.buildings[building_id]

            # remove all rooms under this building
            for room_id in building.rooms:
                if room_id in self.rooms:
                    del self.rooms[room_id]

            del self.buildings[building_id]

    # ---------- room ----------
    def add_room(self, building_id, room):
        if building_id in self.buildings:
            self.buildings[building_id].add_room(room)
            self.rooms[room.room_id] = room
        else:
            print("building not found")

    def get_room(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        return None

    def remove_room(self, room_id):
        if room_id in self.rooms:
            del self.rooms[room_id]

        # also remove from building
        for building in self.buildings.values():
            if room_id in building.rooms:
                building.remove_room(room_id)
                break

    # ---------- demo print ----------
    def print_all(self):
        print("Buildings:", list(self.buildings.keys()))
        print("Rooms:", list(self.rooms.keys()))


# ---------- demo 
def main():
    import time   # only used for performance demo

    system = LookupSystem()

    # add buildings
    b1 = Building("ICT", "ICT Building", (0, 0))
    b2 = Building("ENG", "Engineering", (1, 1))

    system.add_building(b1)
    system.add_building(b2)

    # add rooms
    r1 = Room("ICT-121", 100, "lecture")
    r2 = Room("ENG-201", 50, "lab")

    system.add_room("ICT", r1)
    system.add_room("ENG", r2)

    # lookup existing
    print("Find ICT:", system.get_building("ICT"))
    print("Find ICT-121:", system.get_room("ICT-121"))

    # lookup missing
    print("Find SCI:", system.get_building("SCI"))
    print("Find XXX:", system.get_room("XXX"))

    # remove
    system.remove_room("ICT-121")
    print("After remove ICT-121:", system.get_room("ICT-121"))

    system.remove_building("ENG")
    print("After remove ENG:", system.get_building("ENG"))

    system.print_all()

    # ---------- performance demo ----------
    print("\n--- Performance Test ---")

    start = time.time()
    system.get_building("ICT")
    end = time.time()
    print("Lookup time (small data):", end - start)

    # add many buildings
    for i in range(10000):
        b = Building("B" + str(i), "Building" + str(i), (i, i))
        system.add_building(b)

    start = time.time()
    system.get_building("B9999")
    end = time.time()
    print("Lookup time (large data):", end - start)

    print("Lookup time is similar -> close to O(1)")


if __name__ == "__main__":
    main()