# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime

class Range(object):
    sigma = None

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, other):
        return self._start < other < self._end

    def __repr__(self):
        return

    def _diff(self, a, b):
        return abs(a - b) >= self.sigma

    @property
    def _start(self):
        return self.start - self.sigma

    @property
    def _end(self):
        return self.end + self.sigma

    @property
    def is_empty(self):
        return not self._diff(self.start, self.end)

class DatetimeRange(Range):
    sigma = datetime.timedelta(microseconds=1)

class DateRange(Range):
    def __init__(self, start, end):
        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()
        super(DateRange, self).__init__(start, end)

class IntegerRange(Range):
    sigma = 0.1



