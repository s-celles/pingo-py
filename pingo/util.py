import collections
from .compat import (UserDict, iterkeys)


class StrKeyDict(UserDict):
    """StrKeyDict always converts non-string keys to `str`

    Tests for item retrieval using `d[key]` notation::

        >>> d = StrKeyDict([('2', 'two'), ('4', 'four')])
        >>> d['2']
        'two'
        >>> d[4]
        'four'
        >>> d[1]
        Traceback (most recent call last):
          ...
        KeyError: '1'

    Tests for the `in` operator::

        >>> 2 in d
        True
        >>> 1 in d
        False

    Test for item assignment using non-string key::

        >>> d[0] = 'zero'
        >>> d['0']
        'zero'

    Test for case-insensitive retrieval::

        >>> d['A0'] = 'A-zero'
        >>> d['a0']
        'A-zero'
        >>> del d['A0']

    Tests for update using a `dict` or a sequence of pairs::

        >>> d.update({6:'six', '8':'eight'})
        >>> sorted(d.keys())
        ['0', '2', '4', '6', '8']
        >>> d.update([(10, 'ten'), ('12', 'twelve')])
        >>> sorted(d.keys())
        ['0', '10', '12', '2', '4', '6', '8']
        >>> d.update([1, 3, 5])
        Traceback (most recent call last):
          ...
        TypeError: 'int' object is not iterable

    """

    def normalize(self, key):
        return str(key).upper()

    def __missing__(self, key):
        if isinstance(key, str) and key == self.normalize(key):
            raise KeyError(key)
        return self[self.normalize(key)]

    def __contains__(self, key):
        return self.normalize(key) in self.data

    def __setitem__(self, key, item):
        self.data[self.normalize(key)] = item

    def __iter__(self):
        return iterkeys(self)

    def update(self, iterable=None, **kwds):
        if iterable is not None:
            if isinstance(iterable, collections.Mapping):
                pairs = iterable.items()
            else:
                pairs = ((k, v) for k, v in iterable)
            for key, value in pairs:
                self[key] = value
        if kwds:
            self.update(kwds)


# Decorator
# def mode_restricted(mode):
#     def restriction_decorator(method):
#         def method_wrapper(self, *args, **kwargs):
#             if self.mode != mode:
#                 raise WrongPinMode()
#             return method(self, *args, **kwargs)
#         return method_wrapper
#     return mode_restricted
