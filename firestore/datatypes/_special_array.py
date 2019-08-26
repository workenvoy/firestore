import sys


from firestore.datatypes.base import Base


class SpecialArray(list):
    """
    Special Array hacked together quickly to deliver WB and provide
    support for array of refernces and other array based operations
    on python firestore
    """
    def __init__(self, *args, **kwargs):
        self._data = list(*args)
        self.expected = False
        super(SpecialArray, self).__init__(*args, **kwargs)
    
    def __contains__(self, item):
        return item in self._data
    
    def __eq__(self, comparator):
        return self._data == comparator
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __delitem__(self, key):
        del(self._data[key])
    
    def __ge__(self, comparator):
        return self._data >= comparator
    
    def __iter__(self):
        for datum in self._data:
            yield datum
    
    def __le__(self, comparator):
        return self._data <= comparator
    
    def __reversed__(self):
        reversible = self._data[::-1]
        for datum in reversible:
            yield datum
    
    def __ne__(self, comparator):
        return self._data != comparator

    def __str__(self):
        return str(self._data)
    
    def append(self, value):
        return self._data.append(value)
    
    def clear(self):
        self._data.clear()
    
    def count(self, item):
        return self._data.count(item)
    
    def extend(self, iterable):
        self._data.extend(iterable)
    
    def index(self, item, start=0, stop=sys.maxsize):
        return self._data.index(item, start, stop)
    
    def insert(self, index, obj):
        self._data.insert(index, obj)
    
    def pop(self, index=-1):
        return self._data.pop(index)
    
    def remove(self, value):
        self._data.remove(value)
    
    def reverse(self):
        self._data.reverse()
    
    def sort(self, key=None, reverse=False):
        self._data.sort(key, reverse)
