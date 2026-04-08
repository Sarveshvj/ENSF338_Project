from datetime import datetime


class Booking:
    def __init__(self, booking_id: int, room_id: str, event_name: str, start_time: datetime):
        self.booking_id = booking_id
        self.room_id = room_id
        self.event_name = event_name
        self.start_time = start_time

    def __str__(self):
        return f"[ID: {self.booking_id}] {self.event_name} | Room: {self.room_id} | {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class AVLNode:
    def __init__(self, booking: Booking):
        self.booking = booking
        self.key = booking.start_time   # sorted by start time
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node: AVLNode) -> int:
        return node.height if node else 0

    def _balance_factor(self, node: AVLNode) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node: AVLNode):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self._update_height(z)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        self._update_height(node)
        bf = self._balance_factor(node)

        # Left-Left
        if bf > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        # Left-Right
        if bf > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-Right
        if bf < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        # Right-Left
        if bf < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _insert(self, node: AVLNode, booking: Booking) -> AVLNode:
        if node is None:
            return AVLNode(booking)
        if booking.start_time < node.key:
            node.left = self._insert(node.left, booking)
        elif booking.start_time > node.key:
            node.right = self._insert(node.right, booking)
        else:
            # same timestamp: go right
            node.right = self._insert(node.right, booking)
        return self._rebalance(node)

    def insert(self, booking: Booking):
        self.root = self._insert(self.root, booking)

    def _lookup(self, node: AVLNode, start_time: datetime):
        if node is None:
            return None
        if start_time == node.key:
            return node.booking
        elif start_time < node.key:
            return self._lookup(node.left, start_time)
        else:
            return self._lookup(node.right, start_time)

    def lookup(self, start_time: datetime):
        return self._lookup(self.root, start_time)

    def _inorder(self, node: AVLNode, result: list):
        if node:
            self._inorder(node.left, result)
            result.append(node.booking)
            self._inorder(node.right, result)

    def get_all_sorted(self) -> list:
        result = []
        self._inorder(self.root, result)
        return result
    
    def _print_tree(self, node: AVLNode, prefix: str = "", is_left: bool = True):
        if node is None:
            return
        connector = "L--- " if is_left else "R--- "
        bf = self._balance_factor(node)
        print(f"{prefix}{connector}[{node.booking.event_name} | {node.key.strftime('%H:%M')} | h={node.height} | bf={bf}]")
        new_prefix = prefix + ("     " if is_left else "     ")
        self._print_tree(node.left,  new_prefix, True)
        self._print_tree(node.right, new_prefix, False)

    def print_tree(self):
        if self.root is None:
            print("  (empty tree)")
            return
        bf = self._balance_factor(self.root)
        print(f"ROOT: [{self.root.booking.event_name} | {self.root.key.strftime('%H:%M')} | h={self.root.height} | bf={bf}]")
        self._print_tree(self.root.left,  "  ", True)
        self._print_tree(self.root.right, "  ", False)

    def _check_balance(self, node: AVLNode) -> bool:
        if node is None:
            return True
        bf = self._balance_factor(node)
        if abs(bf) > 1:
            return False
        return self._check_balance(node.left) and self._check_balance(node.right)

    def is_balanced(self) -> bool:
        return self._check_balance(self.root)

def simulate_avl():
    bookings = [
        Booking(1,  "ICT-101",  "ENSF 338 Lecture",         datetime(2026, 4, 6,  8,  0)),
        Booking(2,  "ICT-201",  "ENSF 331 Lab",             datetime(2026, 4, 6,  9,  0)),
        Booking(3,  "ENG-305",  "ENEL 353 Tutorial",        datetime(2026, 4, 6, 10,  0)),
        Booking(4,  "LIB-01",   "Study Group A",            datetime(2026, 4, 6, 11,  0)),
        Booking(5,  "SCI-210",  "CHEM 201 Lecture",         datetime(2026, 4, 6, 12,  0)),
        Booking(6,  "ICT-101",  "ENSF 480 Lecture",         datetime(2026, 4, 6, 13,  0)),
        Booking(7,  "MFH-12",   "Club Meeting",             datetime(2026, 4, 6, 14,  0)),
        Booking(8,  "ENG-101",  "ENGG 200 Lecture",         datetime(2026, 4, 6, 15,  0)),
        Booking(9,  "LIB-02",   "Study Group B",            datetime(2026, 4, 6, 16,  0)),
        Booking(10, "GYM-01",   "Fitness Class",            datetime(2026, 4, 6, 17,  0)),
    ]

    tree = AVLTree()

    print("\n")
    print("BEFORE INSERTIONS")
    print("\n")

    tree.print_tree()
    print(f"Balanced: {tree.is_balanced()}")

    print("\n")
    print("INSERTING BOOKINGS (adversarial: chronological order)")
    print("\n")

    for b in bookings:
        tree.insert(b)
        bf = tree._balance_factor(tree.root)
        print(f"  Inserted: {b.event_name} at {b.start_time.strftime('%H:%M')} "
              f"| root height={tree.root.height} | root bf={bf} | balanced={tree.is_balanced()}")

    print("\n")
    print("AFTER ALL INSERTIONS")
    print("\n")
    tree.print_tree()
    print(f"\nBalanced: {tree.is_balanced()}")

    print("\n")
    print("IN-ORDER TRAVERSAL (should be sorted by time)")
    print("\n")
    for b in tree.get_all_sorted():
        print(f"  {b}")

    print("\n")
    print("LOOKUP DEMO")
    print("\n")
    search_time = datetime(2026, 4, 6, 11, 0)
    result = tree.lookup(search_time)
    print(f"  Lookup {search_time.strftime('%H:%M')} -> {result if result else 'Not found'}")

    missing_time = datetime(2026, 4, 6, 18, 0)
    result2 = tree.lookup(missing_time)
    print(f"  Lookup {missing_time.strftime('%H:%M')} -> {result2 if result2 else 'Not found'}")


if __name__ == "__main__":
    simulate_avl()