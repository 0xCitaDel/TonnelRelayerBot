from typing import Dict, List, Optional, Set


class NewElementsTracker:

    def __init__(self):
        """Tracker with a fixed-size memory of last seen items."""
        self.known_items: Set[frozenset] = set()

    def _hash_dict_recursive(self, item: Dict):
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

    def check_new_elements(self, data: Optional[List[Dict]]) -> list:
        """Check for new elements while keeping only recent ones."""
        new_items = []
        new_item_hashes = set()

        if data:
            for item in data:
                hashed = self._hash_dict_recursive(item)
                new_item_hashes.add(hashed)

                if hashed not in self.known_items:
                    new_items.append(item)

            self.known_items = new_item_hashes

        return new_items
