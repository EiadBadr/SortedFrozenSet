from collections.abc import Sequence, Set
from itertools import chain
from bisect import bisect_left

class SortedFrozenSet(Sequence, Set):
    def __init__(self, items = None): 
        # return sorted non-duplicate list:   
        self._items = tuple(sorted(
            set(items) if (items is not None)
            else set()
        )
        )

    # container protocol:
    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False

        index = bisect_left(self._items , item)
        return (index != len(self._items)) and self._items[index] == item

    # sized protocol:
    def __len__(self):
        return len(self._items)

    # iterable protocol:
    def __iter__(self):
        return iter(self._items)

    # sequence protocol:
    def __getitem__(self, index):
        #print(index)
        #print(type(index))
        result = self._items[index]
        return ( 
            SortedFrozenSet(result) if isinstance(index, slice)
            else result
            )

    def __repr__(self):
        return "{type}({arg})".format(
            type = type(self).__name__,
            arg= ("[{}]".format(
                ", ".join(map(repr,self._items )))
                if self._items else ""
                )
        )

    # reference equality (equality of identity) rather than equivalence (equality of value) 
    def __eq__(self, rhs):
        if not isinstance(rhs, type(self)):
            return NotImplemented
        return self._items == rhs._items

    def __hash__(self):
        return hash(
            (type(self),self._items))
    
    def __add__(self, rhs):
        if not isinstance(rhs , type(self)):
            return NotImplemented
        return SortedFrozenSet(
            chain(self._items, rhs._items)
        )
    
    def __mul__(self, rhs):
        return self if rhs > 0 else SortedFrozenSet() 
    
    def __rmul__(self, lhs):
        return self * lhs

    def count(self, item):
        # index = bisect_left(self._items , item)
        # found = (index != len(self._items)) and self._items[index] == item
        return int(item in self)

    def index(self, item):
        index = bisect_left(self._items , item)
        if (index != len(self._items)) and self._items[index] == item:
            return index
        raise ValueError(f"{item!r} is not found")
    
    def issubset(self, iterable):
        return self <= SortedFrozenSet(iterable)

    def issuperset(self, iterable):
        return self >= SortedFrozenSet(iterable)

    def intersection(self, iterable):
        return self & SortedFrozenSet(iterable)

    def union(self, iterable):
        return self | SortedFrozenSet(iterable)

    def symmetric_difference(self, iterable):
        return self ^ SortedFrozenSet(iterable)

    def difference(self, iterable):
        return self - SortedFrozenSet(iterable)
    #being regular method there is no opportuniy for fallback mechanism , like index
    # immutable extended optional sequence is:
    # add, radd , mul, rmul

