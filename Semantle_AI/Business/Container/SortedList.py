import random

import numpy as np
from Semantle_AI.Business.Container.MyItem import MyItem
from typing import List, Optional


class SortedList:
    def __init__(self, initial_items=None):
        self.items = initial_items if initial_items is not None else []
        self.sort()  # Ensure the list is sorted after initialization

    def __contains__(self, item: MyItem):
        return item in self.items

    def __hash__(self):
        return hash(tuple(self.items))

    def __eq__(self, other):
        if isinstance(other, SortedList):
            return self.items == other.items
        return False

    def __repr__(self):
        return str(self.items)

    def __iter__(self):
        self._iter_idx = 0
        return self

    def __next__(self):
        if self._iter_idx < len(self.items):
            result = self.items[self._iter_idx]
            self._iter_idx += 1
            return result
        else:
            raise StopIteration

    def __len__(self):
        return len(self.items)

    def add(self, item: MyItem):
        self.items.append(item)

    def remove(self, item: MyItem):
        if item in self.items:
            self.items.remove(item)
            return item  # Return the removed item
        else:
            return None  # Return None if the item is not in the list

    def clear(self):
        self.items = []

    def sort(self):
        self.items = list(np.sort(np.array(self.items)))

    def update_all(self, modification_func):
        self.items = [modification_func(item) for item in self.items]
        self.sort()

    def pick_random(self):
        if not self.items:
            raise ValueError("List is empty")
        item = random.choice(self.items)
        self.items.remove(item)
        return item

    def get_by_index(self, index):
        if index < 0 or index >= len(self.items):
            raise IndexError("Index out of range")
        return self.items[index]

    def get_by_value(self, value):
        for item in self.items:
            if item == value:
                return item
        return None  # Return None if no item matches the value

    def get_last_item(self) -> Optional[MyItem]:
        if self.items:
            item = self.items[-1]
            self.remove(item)
            return item
        else:
            return None

    @staticmethod
    def change_weight(item: MyItem, value: int):
        item.weight = value
        return item