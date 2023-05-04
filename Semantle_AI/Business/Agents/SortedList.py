# import sys
#
#
# class SortedList:
#     def __init__(self, items):
#         self.sorted_items = sorted(items, key=lambda x: x.weight)
#         if len(items)>0:
#             self.min_value = self.sorted_items[0].weight
#         else:
#             self.min_value = sys.maxsize
#
#     def pop_min(self):
#         min_item = self.sorted_items.pop(0)
#         if min_item.weight == self.min_value:
#             self.min_value = self.sorted_items[0].weight
#         return min_item
#
#     def __repr__(self):
#         return f'SortedList({self.sorted_items})'
#
#     def __len__(self):
#         return len(self.sorted_items)
#
#     def __getitem__(self, index):
#         return self.sorted_items[index]
#
#     def insert(self, item):
#         self.sorted_items.append(item)
#         self.sorted_items.sort(key=lambda x: x.weight)
#         if item.weight < self.min_value:
#             self.min_value = item.weight
#
#     def remove(self, item):
#         self.sorted_items.remove(item)
#         if item.weight == self.min_value:
#             self.min_value = self.sorted_items[0].weight
#
#     def modify_weight(self, item, new_weight):
#         # find the item in the list and update its weight
#         found = False
#         for i, x in enumerate(self.sorted_items):
#             if x == item:
#                 found=True
#                 old_weight = x.weight
#                 x.weight = new_weight
#                 break
#
#         # sort the list by the new weights
#         self.sorted_items.sort(key=lambda x: x.weight)
#
#         # update the minimum value if necessary
#         if found and old_weight == self.min_value and new_weight >= self.min_value:
#             self.min_value = self.sorted_items[0].weight
#         elif new_weight < self.min_value:
#             self.min_value = new_weight
#
#     def get_min_value(self):
#         return self.min_value
#
#     def clear(self):
#         self.sorted_items = []
#         self.min_value = float('inf')
#
#     def __iter__(self):
#         return iter(self.sorted_items)
#
#     def __repr__(self):
#         return f'SortedList({self.sorted_items}, min_value={self.min_value})'