# import the MyList and MyItem classes
from Semantle_AI.Business.Agents.Data import MyItem
from Semantle_AI.Business.Agents.SortedList import SortedList

# create some MyItem objects
item1 = MyItem('foo', 3)
item2 = MyItem('bar', 2)
item3 = MyItem('baz', 1)

# create a MyList object and add the items
mylist = SortedList([item1, item2, item3])

# print the original list
print(mylist)  # MyList(items=[foo (3), bar (2), baz (1)], min_value=1)

# iterate over the list and update the weights
for item in mylist:
    if item.weight == 1:
        mylist.modify_weight(item, item.weight + 3)

# update the minimum value after modifying the weights
mylist.modify_weight(item1, item1.weight)

# print the updated list and minimum value
print(mylist)  # MyList(items=[foo (4), bar (3), baz (2)], min_value=2)
