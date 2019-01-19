class fraction:
    def __init__(self, top, bottom):
        self.top = top
        self.bottom = bottom

 def __str__(self):
        return '%d/%d' % (self.top, self.bottom)

    def __add__(self, other):
        return fraction(self.top + other.top, self.bottom)

    def __pow__(self, n):
        return fraction(self.top ** n, self.bottom ** n)

    def __del__(self):
        print('del', self)
        self.top = 0
        self.bottom = 0

a = fraction(1,3)
b = fraction(1,3)
c = a + b