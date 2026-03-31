# Feature 2.3 - Room and Event Booking System
# Uses a BST to keep bookings sorted by datetime

from datetime import datetime, timedelta
import random


class Booking:
    _id_counter = 0

    def __init__(self, room_id, date, start_time, end_time, event_name):
        Booking._id_counter += 1
        self.booking_id = Booking._id_counter
        self.room_id = room_id
        self.date = date              # "YYYY-MM-DD"
        self.start_time = start_time  # "HH:MM"
        self.end_time = end_time      # "HH:MM"
        self.event_name = event_name

        # combine into one datetime so BST can compare easily
        self.datetime_key = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")

    def __str__(self):
        return (f"[Booking #{self.booking_id}] {self.event_name} | "
                f"Room: {self.room_id} | {self.date} {self.start_time}-{self.end_time}")


class BSTNode:
    def __init__(self, booking):
        self.booking = booking
        self.key = booking.datetime_key
        self.left = None
        self.right = None


class BookingBST:
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, booking):
        new_node = BSTNode(booking)
        if self.root is None:
            self.root = new_node
            self.size += 1
            return

        current = self.root
        while True:
            if booking.datetime_key <= current.key:
                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right
        self.size += 1

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.booking)
        self._inorder(node.right, result)

    def get_all_sorted(self):
        result = []
        self._inorder(self.root, result)
        return result

    # need to search all nodes since BST is keyed on datetime not id
    def _find_by_id(self, node, booking_id):
        if node is None:
            return None
        if node.booking.booking_id == booking_id:
            return node.booking
        left = self._find_by_id(node.left, booking_id)
        if left:
            return left
        return self._find_by_id(node.right, booking_id)

    def search_by_id(self, booking_id):
        return self._find_by_id(self.root, booking_id)

    def _get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def delete(self, booking_id):
        target = self.search_by_id(booking_id)
        if target is None:
            print(f"Booking #{booking_id} not found.")
            return False
        self.root = self._delete_helper(self.root, target.datetime_key, booking_id)
        self.size -= 1
        return True

    def _delete_helper(self, node, key, bid):
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_helper(node.left, key, bid)
        elif key > node.key:
            node.right = self._delete_helper(node.right, key, bid)
        else:
            # keys match - make sure its the right booking though
            if node.booking.booking_id == bid:
                # case 1 and 2: no child or one child
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                # case 3: two children, get inorder successor
                successor = self._get_min(node.right)
                node.booking = successor.booking
                node.key = successor.key
                node.right = self._delete_helper(
                    node.right, successor.key, successor.booking.booking_id
                )
            else:
                # same datetime but different booking, could be on either side
                node.left = self._delete_helper(node.left, key, bid)
                node.right = self._delete_helper(node.right, key, bid)
        return node

    def range_query(self, start_dt, end_dt):
        # returns all bookings with datetime_key in [start_dt, end_dt]
        result = []
        self._range_helper(self.root, start_dt, end_dt, result)
        return result

    def _range_helper(self, node, start, end, result):
        if node is None:
            return
        # prune left if nothing there could be in range
        if node.key > start:
            self._range_helper(node.left, start, end, result)
        if start <= node.key <= end:
            result.append(node.booking)
        if node.key < end:
            self._range_helper(node.right, start, end, result)

    def find_next_after(self, dt):
        # find the soonest booking after dt
        best = [None]
        self._next_helper(self.root, dt, best)
        return best[0]

    def _next_helper(self, node, dt, best):
        if node is None:
            return
        if node.key > dt:
            if best[0] is None or node.key < best[0].datetime_key:
                best[0] = node.booking
            self._next_helper(node.left, dt, best)
        else:
            self._next_helper(node.right, dt, best)


class BookingSystem:
    def __init__(self):
        self.bst = BookingBST()
        self.bookings_map = {}  # id -> booking for quick access

    def add_booking(self, room_id, date, start_time, end_time, event_name):
        booking = Booking(room_id, date, start_time, end_time, event_name)
        self.bst.insert(booking)
        self.bookings_map[booking.booking_id] = booking
        return booking

    def remove_booking(self, booking_id):
        if booking_id not in self.bookings_map:
            print(f"Booking #{booking_id} doesn't exist.")
            return False
        ok = self.bst.delete(booking_id)
        if ok:
            del self.bookings_map[booking_id]
        return ok

    def get_booking(self, booking_id):
        return self.bookings_map.get(booking_id, None)

    def get_bookings_on_date(self, date_str):
        start = datetime.strptime(f"{date_str} 00:00", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{date_str} 23:59", "%Y-%m-%d %H:%M")
        return self.bst.range_query(start, end)

    def get_bookings_in_range(self, start_date, start_time, end_date, end_time):
        start_dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
        return self.bst.range_query(start_dt, end_dt)

    def next_upcoming(self, date=None, time=None):
        if date and time:
            now = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        else:
            now = datetime.now()
        return self.bst.find_next_after(now)

    def get_all(self):
        return self.bst.get_all_sorted()


def generate_bulk_bookings(system, count=100):
    # makes a bunch of test bookings across April 2026
    rooms = ["ICT-121", "ICT-219", "ENG-201", "ENG-305", "SCI-101",
             "SCI-215", "LIB-A1", "LIB-B2", "STU-100", "MFH-110"]
    events = ["Lecture", "Lab", "Study Group", "Workshop",
              "Seminar", "Office Hours", "Club Meeting", "Exam Review",
              "Tutorial", "Guest Talk"]

    base = datetime(2026, 4, 1)
    for i in range(count):
        day = random.randint(0, 29)
        date_str = (base + timedelta(days=day)).strftime("%Y-%m-%d")
        hour = random.randint(8, 18)
        start = f"{hour:02d}:00"
        end = f"{min(hour + random.randint(1, 2), 20):02d}:00"
        room = random.choice(rooms)
        name = f"{random.choice(events)} - {room}"

        b = Booking(room, date_str, start, end, name)
        system.bst.insert(b)
        system.bookings_map[b.booking_id] = b


#Manual Testing
if __name__ == "__main__":
    system = BookingSystem()

    # Adding some bookings
    b1 = system.add_booking("ICT-121", "2026-04-05", "09:00", "10:30", "ENSF 338 Lecture")
    b2 = system.add_booking("ICT-219", "2026-04-05", "11:00", "12:00", "CPSC 231 Lab")
    b3 = system.add_booking("ENG-201", "2026-04-05", "13:00", "14:30", "Study Group")
    b4 = system.add_booking("SCI-101", "2026-04-05", "10:00", "11:00", "Physics Seminar")
    b5 = system.add_booking("ICT-121", "2026-04-06", "09:00", "10:00", "ENSF 338 Tutorial")
    b6 = system.add_booking("LIB-A1",  "2026-04-07", "14:00", "16:00", "Club Meeting")
    print("Added 6 bookings\n")

    # Get all bookings on April 5
    print("--- All bookings on April 5 ---")
    for b in system.get_bookings_on_date("2026-04-05"):
        print(f"  {b}")

    # Range query: 10am to 2pm on April 5
    print("\n--- Bookings between 10:00-14:00 on April 5 ---")
    for b in system.get_bookings_in_range("2026-04-05", "10:00", "2026-04-05", "14:00"):
        print(f"  {b}")

    # Next upcoming after 10:30am April 5
    print(f"\n--- Next event after April 5 10:30 ---")
    nxt = system.next_upcoming("2026-04-05", "10:30")
    print(f"  {nxt}")

    # Remove booking #2
    print(f"\n--- Removing booking #2 ---")
    system.remove_booking(2)
    print("April 5 after removal:")
    for b in system.get_bookings_on_date("2026-04-05"):
        print(f"  {b}")

    # Try removing something that doesn't exist
    print()
    system.remove_booking(999)

    # Bulk test - 100 bookings
    print("\n--- Generating 100 bulk bookings ---")
    generate_bulk_bookings(system, 100)
    print(f"Total bookings now: {len(system.get_all())}")

    # Show a sample day from bulk
    sample = system.get_bookings_on_date("2026-04-15")
    print(f"\nBookings on April 15: {len(sample)}")
    for b in sample:
        print(f"  {b}")
