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


@total_ordering
class Range(object):
    sigma = None
    kind = None

    def __init__(self, start, end):
        if start > end:
            start, end = end, start

        self.start = start
        self.end = end

    def __contains__(self, timepoint):
        return self._start < timepoint < self._end

    def includes(self, other):
        return other.start in self and other.end in self

    def overlaps(self, other):
        return self.start in other or self.end in other or self.includes(other)

    def _diff(self, a, b):
        return abs(a - b) >= self.sigma

    def __eq__(self, other):
        if self.kind is not other.kind:
            return False
        if not isinstance(other, type(self)):
            return False
        if self._diff(self.start, other.start):
            return False
        if self._diff(self.end, other.end):
            return False
        return True

    def __lt__(self, other):
        if self.kind is not other.kind:
            return cmp(self.kind, other.kind)
        return self.duration < other.duration

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
    def _end(self):
        """
        Sigma fudge for simpler comparisons.
        """
        return self.end + self.sigma

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



"""

For most applications this is all you need. But certain situations suggest other useful behaviors. One it to find out what gap exists between two ranges.

class DateRange...
    public DateRange gap(DateRange arg){
        if (this.overlaps(arg)) return DateRange.EMPTY;
        DateRange lower, higher;
        if (this.compareTo(arg) < 0) {
            lower = this;
            higher = arg;
        }
        else {
            lower = arg;
            higher = this;
        }
        return new DateRange(lower.end.addDays(1), higher.start.addDays(-1));
    }
    public int compareTo(Object arg) {
        DateRange other = (DateRange) arg;
        if (!start.equals(other.start)) return start.compareTo(other.start);
        return end.compareTo(other.end);
    }
Another is to detect whether two date ranges abut each other.

class DateRange...
    public boolean abuts(DateRange arg) {
        return !this.overlaps(arg) && this.gap(arg).isEmpty();
    }

And to see if a group of ranges completly partitions another range.

class DateRange...
    public boolean partitionedBy(DateRange[] args) {
        if (!isContiguous(args)) return false;
        return this.equals(DateRange.combination(args));
    }
    public static DateRange combination(DateRange[] args) {
        Arrays.sort(args);
        if (!isContiguous(args)) throw new IllegalArgumentException("Unable to combine date ranges");
        return new DateRange(args[0].start, args[args.length -1].end);
    }
    public static boolean isContiguous(DateRange[] args) {
        Arrays.sort(args);
        for (int i=0; i<args.length - 1; i++) {
                if (!args[i].abuts(args[i+1])) return false;
        }
        return true;
    }

"""