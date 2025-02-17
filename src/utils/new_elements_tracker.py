from collections import deque


class NewElementsTracker:

    def __init__(self, max_size=10):
        """Tracker with a fixed-size memory of last seen items."""
        self.known_items = set()
        self.recent_items = deque(
            maxlen=max_size
        )

    def _hash_dict(self, item):
        """Generate a unique, immutable hash for a dictionary."""
        return frozenset(item.items())

    def _hash_dict_recursive(self, item):
        """Recursively converts a dictionary into a hashable, immutable frozenset."""

        def make_hashable(obj):
            if isinstance(obj, dict):
                return frozenset(
                    (key, make_hashable(value)) for key, value in obj.items()
                )
            elif isinstance(obj, list):  # Convert lists to tuples to make them hashable
                return tuple(make_hashable(x) for x in obj)
            return obj  # Immutable types remain unchanged

        return make_hashable(item)

    def check_new(self, new_data):
        """Check for new elements while keeping only recent ones."""
        new_items = []
        for item in new_data:
            hashed = self._hash_dict_recursive(item)
            if hashed not in self.known_items:
                new_items.append(item)

                # Add new item to tracking (remove oldest if over limit)
                self.recent_items.append(hashed)
                self.known_items.add(hashed)

        # Remove old items that fell out of `deque`
        self.known_items.intersection_update(self.recent_items)

        return new_items
