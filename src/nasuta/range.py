# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
from functools import total_ordering

class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


@total_ordering
class _Max(object):
    def __sub__(self, other):
        return other

    def __add__(self, other):
        return self

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return False
        return True

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __abs__(self):
        return self

@total_ordering
class _Min(object):
    def __sub__(self, other):
        return self

    def __add__(self, other):
        return other

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return False
        return True

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __abs__(self):
        return self

class InvalidRange(ValueError):
    pass

@total_ordering
class Range(object):
    """
    `sigma` is the largest "difference" that makes no difference.
      This is needed for continuuous ranges like floats, where
      precision can be lost.
    `kind` is the type of start/end,
    """
    sigma = None
    kind = None

    def __init__(self, start, end):
        if start > end:
            raise InvalidRange()

        self.start = start
        self.end = end

    def __contains__(self, timepoint):
        if self.is_empty:
            return False
        return self._start < timepoint < self._end

    def includes(self, other):
        if other.is_empty:
            return False
        return other.start in self and other.end in self

    def overlaps(self, other):
        return self.includes(other) or self._start in other or self.end_ in other

    def _diff(self, a, b):
        if isinstance(a, self._sentinels) or isinstance(b, self._sentinels):
            return not isinstance(a, type(b))
        return abs(a - b) >= self.sigma

    def __eq__(self, other):
        if self.kind is not other.kind:
            return NotImplemented
        if not isinstance(other, type(self)):
            return NotImplemented
        if self._diff(self.start, other.start):
            return False
        if self._diff(self.end, other.end):
            return False
        return True

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        if self._diff(self.start, other.start):
            return self.start < other.start

        if self._diff(self.end, other.end):
            return self.end < other.end

        return False

    def gap(self, other):
        if self.overlaps(other):
            return self.empty

        if self < other:
            lower, higher = self, other
        else:
            lower, higher = other, self

        if self._diff(lower.end, higher.start):
            return type(self)(lower.end, higher.start)
        else:
            return self.empty

    def abuts(self, other):
        return (not self.overlaps(other)) and self.gap(other) == self.empty



    @classproperty
    @classmethod
    def empty(cls):
        return cls(cls.min, cls.min)

    @property
    def duration(self):
        if (isinstance(self.start, self._sentinels) or
            isinstance(self.end, self._sentinels)):
            return self.max
        return self.end - self.start

    @property
    def _start(self):
        """
        Sigma fudge for simpler comparisons.
        """
        return self.start - self.sigma

    @property
    def start_(self):
        return self.start + self.sigma

    @property
    def _end(self):
        """
        Sigma fudge for simpler comparisons.
        """
        return self.end + self.sigma

    @property
    def end_(self):
        return self.end - self.sigma

    @property
    def is_empty(self):
        return not self._diff(self.start, self.end)

    @classproperty
    @classmethod
    def min(cls):
        if hasattr(cls, '_min'):
            return cls._min

        class Min(_Min):
            pass

        cls._min = Min()
        return cls._min

    @classproperty
    @classmethod
    def max(cls):
        if hasattr(cls, '_max'):
            return cls._max

        class Max(_Max):
            pass

        cls._max = Max()
        return cls._max

    @classproperty
    @classmethod
    def _sentinels(cls):
        return (type(cls.min), type(cls.max))

    @classmethod
    def up_to(cls, end):
        return cls(cls.min, end)

    @classmethod
    def starting_from(cls, start):
        return cls(start, cls.max)

    def __repr__(self):
        if self.is_empty:
            return "[]"
        else:
            return "{0} - {1}".format(self.start, self.end)


class DatetimeRange(Range):
    sigma = datetime.timedelta(microseconds=1)
    kind = datetime.datetime

class DateRange(Range):
    sigma = datetime.timedelta(hours=1)
    kind = datetime.date

    def __init__(self, start, end):
        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()
        super(DateRange, self).__init__(start, end)

class IntegerRange(Range):
    sigma = 0.1
    kind = int
