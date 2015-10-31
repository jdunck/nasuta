class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, other):
        return self.start <= other <= self.end
