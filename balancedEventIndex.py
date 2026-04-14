from datetime import datetime


class Booking:
    """
    Represents a single room booking in the campus system.

    Stores the booking ID, room ID, event name, and start time.
    The start time is used as the key for ordering in the AVL tree.
    """

    def __init__(self, booking_id: int, room_id: str, event_name: str, start_time: datetime):
        """
        Initialize a Booking object.

        Args:
            booking_id: Unique identifier for the booking.
            room_id: ID of the room being booked (e.g. 'ICT-101').
            event_name: Name of the event or session.
            start_time: Scheduled start time of the booking.
        """
        self.booking_id = booking_id
        self.room_id = room_id
        self.event_name = event_name
        self.start_time = start_time

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the booking.
        """
        return (f"[ID: {self.booking_id}] {self.event_name} | "
                f"Room: {self.room_id} | {self.start_time.strftime('%Y-%m-%d %H:%M')}")


class AVLNode:
    """
    A single node in the AVL tree.
    Stores a Booking object, a key (start_time) for comparisons,
    left and right child pointers, and the node's height used
    for computing balance factors during rebalancing.
    """
    def __init__(self, booking: Booking):
        """
        Initialize an AVLNode with a booking and height of 1.

        Args:
            booking: The Booking object stored in this node.
        """
        self.booking = booking
        self.key = booking.start_time
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """
    A self-balancing AVL tree indexed by booking start time.
    Guarantees O(log n) insert and lookup at all times by maintaining
    the AVL balance property — every node's left and right subtree
    heights differ by at most 1. Rebalancing is performed after every
    insertion using four rotation cases: Left-Left, Right-Right,
    Left-Right, and Right-Left.
    """
    def __init__(self):
        """Initialize an empty AVL tree."""
        self.root = None

    def _height(self, node: AVLNode) -> int:
        """
        Return the height of a node, or 0 if the node is None.

        Args:
            node: The AVLNode to check.

        Returns:
            Height of the node, or 0 if None.
        """
        return node.height if node else 0

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Compute the balance factor of a node.
        Balance factor = height(left subtree) - height(right subtree).
        A value outside [-1, 1] means the node is unbalanced.

        Args:
            node: The AVLNode to check.

        Returns:
            The balance factor as an integer, or 0 if node is None.
        """
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node: AVLNode) -> None:
        """
        Recalculate and update the height of a node based on its children.

        Args:
            node: The AVLNode whose height needs updating.
        """
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """
        Perform a right rotation on the subtree rooted at z.

        Used to fix a Left-Left imbalance. The left child y becomes
        the new root of the subtree, and z becomes y's right child.

        Args:
            z: The unbalanced node to rotate around.

        Returns:
            The new root of the subtree after rotation.
        """
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """
        Perform a left rotation on the subtree rooted at z.

        Used to fix a Right-Right imbalance. The right child y becomes
        the new root of the subtree, and z becomes y's left child.

        Args:
            z: The unbalanced node to rotate around.

        Returns:
            The new root of the subtree after rotation.
        """
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        self._update_height(z)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        Rebalance a node if its balance factor is outside [-1, 1].

        Handles all four rotation cases:
            - Left-Left:   single right rotation
            - Left-Right:  left rotate child, then right rotate root
            - Right-Right: single left rotation
            - Right-Left:  right rotate child, then left rotate root

        Args:
            node: The AVLNode to check and potentially rebalance.

        Returns:
            The new root of the subtree after rebalancing.
        """
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
        """
        Recursively insert a booking and rebalance on the way back up.

        Args:
            node: Current node in the recursive traversal.
            booking: The Booking object to insert.

        Returns:
            The new root of the subtree after insertion and rebalancing.
        """
        if node is None:
            return AVLNode(booking)
        if booking.start_time < node.key:
            node.left = self._insert(node.left, booking)
        elif booking.start_time > node.key:
            node.right = self._insert(node.right, booking)
        else:
            # same timestamp: go right to allow duplicate times
            node.right = self._insert(node.right, booking)
        return self._rebalance(node)

    def insert(self, booking: Booking) -> None:
        """Insert a booking into the AVL tree.

        The tree rebalances automatically after insertion to maintain
        O(log n) height at all times.

        Args:
            booking: The Booking object to insert.
        """
        self.root = self._insert(self.root, booking)

    def _lookup(self, node: AVLNode, start_time: datetime):
        """
        Recursively search for a booking by start time.
        Args:
            node: Current node in the recursive traversal.
            start_time: The start time to search for.

        Returns:
            The matching Booking object, or None if not found.
        """
        if node is None:
            return None
        if start_time == node.key:
            return node.booking
        elif start_time < node.key:
            return self._lookup(node.left, start_time)
        else:
            return self._lookup(node.right, start_time)

    def lookup(self, start_time: datetime):
        """Look up a booking by its start time.

        Args:
            start_time: The start time to search for.

        Returns:
            The matching Booking object, or None if not found.
        """
        return self._lookup(self.root, start_time)

    def _inorder(self, node: AVLNode, result: list) -> None:
        """
        Recursively collect all bookings in ascending time order.
        Args:
            node: Current node in the recursive traversal.
            result: List to append bookings to.
        """
        if node:
            self._inorder(node.left, result)
            result.append(node.booking)
            self._inorder(node.right, result)

    def get_all_sorted(self) -> list:
        """
        Return all bookings sorted by start time in ascending order.

        Returns:
            A list of Booking objects ordered by start time.
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _print_tree(self, node: AVLNode, prefix: str = "", is_left: bool = True) -> None:
        """
        Recursively print the tree structure with height and balance factor.
        Args:
            node: Current node in the recursive traversal.
            prefix: Indentation string for the current level.
            is_left: Whether this node is a left child.
        """
        if node is None:
            return
        connector = "L--- " if is_left else "R--- "
        bf = self._balance_factor(node)
        print(f"{prefix}{connector}[{node.booking.event_name} | "
              f"{node.key.strftime('%H:%M')} | h={node.height} | bf={bf}]")
        new_prefix = prefix + "     "
        self._print_tree(node.left,  new_prefix, True)
        self._print_tree(node.right, new_prefix, False)

    def print_tree(self) -> None:
        """
        Print the full AVL tree structure to the terminal.

        Displays each node's event name, time, height, and balance factor.
        Used to visually verify the balance property before and after insertions.
        """
        if self.root is None:
            print("  (empty tree)")
            return
        bf = self._balance_factor(self.root)
        print(f"ROOT: [{self.root.booking.event_name} | "
              f"{self.root.key.strftime('%H:%M')} | h={self.root.height} | bf={bf}]")
        self._print_tree(self.root.left,  "  ", True)
        self._print_tree(self.root.right, "  ", False)

    def _check_balance(self, node: AVLNode) -> bool:
        """
        Recursively verify the AVL balance property for all nodes.

        Args:
            node: Current node in the recursive traversal.

        Returns:
            True if all nodes satisfy the balance property, False otherwise.
        """
        if node is None:
            return True
        bf = self._balance_factor(node)
        if abs(bf) > 1:
            return False
        return self._check_balance(node.left) and self._check_balance(node.right)

    def is_balanced(self) -> bool:
        """
        Check whether the entire tree satisfies the AVL balance property.
        Returns:
            True if every node has a balance factor in [-1, 0, 1], False otherwise.
        """
        return self._check_balance(self.root)

def get_sample_bookings() -> list:
    """
    Return a hardcoded list of 10 bookings inserted in chronological order.
    This is the adversarial case for a plain BST — sorted insertions cause
    it to degenerate into a linked list of height 10. The AVL tree handles
    this correctly, maintaining a height of 4 after all insertions.

    Returns:
        A list of 10 Booking objects in chronological order.
    """
    return [
        Booking(1,  "ICT-101", "ENSF 338 Lecture",   datetime(2026, 4, 6,  8, 0)),
        Booking(2,  "ICT-201", "ENSF 331 Lab",        datetime(2026, 4, 6,  9, 0)),
        Booking(3,  "ENG-305", "ENEL 353 Tutorial",   datetime(2026, 4, 6, 10, 0)),
        Booking(4,  "LIB-01",  "Study Group A",       datetime(2026, 4, 6, 11, 0)),
        Booking(5,  "SCI-210", "CHEM 201 Lecture",    datetime(2026, 4, 6, 12, 0)),
        Booking(6,  "ICT-101", "ENSF 480 Lecture",    datetime(2026, 4, 6, 13, 0)),
        Booking(7,  "MFH-12",  "Club Meeting",        datetime(2026, 4, 6, 14, 0)),
        Booking(8,  "ENG-101", "ENGG 200 Lecture",    datetime(2026, 4, 6, 15, 0)),
        Booking(9,  "LIB-02",  "Study Group B",       datetime(2026, 4, 6, 16, 0)),
        Booking(10, "GYM-01",  "Fitness Class",       datetime(2026, 4, 6, 17, 0)),
    ]

def simulate_avl() -> None:
    """
    Simulate the balanced event index using an AVL tree.
    Demonstrates the balance property before insertions, after each
    individual insertion, and after all insertions. Also demonstrates
    in-order traversal and lookup by start time.
    """
    tree = AVLTree()
    print("\nBEFORE INSERTIONS")
    tree.print_tree()
    print(f"\nBalanced: {tree.is_balanced()}")
    print("\nINSERTING BOOKINGS (adversarial: chronological order)")
    for b in get_sample_bookings():
        tree.insert(b)
        bf = tree._balance_factor(tree.root)
        print(f"  Inserted: {b.event_name} at {b.start_time.strftime('%H:%M')} "
              f"| root height={tree.root.height} | root bf={bf} | balanced={tree.is_balanced()}")

    print("\nAFTER ALL INSERTIONS")
    tree.print_tree()
    print(f"\nBalanced: {tree.is_balanced()}")
    print("\nIN-ORDER TRAVERSAL (should be sorted by time)")
    for b in tree.get_all_sorted():
        print(f"  {b}")

    print("\nLOOKUP DEMO")
    search_time = datetime(2026, 4, 6, 11, 0)
    result = tree.lookup(search_time)
    print(f"  Lookup {search_time.strftime('%H:%M')} -> {result if result else 'Not found'}")

    missing_time = datetime(2026, 4, 6, 18, 0)
    result2 = tree.lookup(missing_time)
    print(f"  Lookup {missing_time.strftime('%H:%M')} -> {result2 if result2 else 'Not found'}")

if __name__ == "__main__":
    simulate_avl()