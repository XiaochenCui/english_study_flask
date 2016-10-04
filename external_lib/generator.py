class YieldPieceOfList(object):
    def __init__(self, l: list, n: int):
        self.l = l
        self.n = n
        self.g = None

    def get_n_enum(self):
        i = 0
        while i * self.n < len(self.l):
            yield self.l[i * self.n: (i + 1) * self.n]
            i += 1

    def function(self):
        if not self.g:
            self.g = self.get_n_enum()
        try:
            return self.g.__next__()
        except StopIteration:
            return None


if __name__ == '__main__':
    l = [i for i in range(100)]
    g = YieldPieceOfList(l, 9)
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
    print(g.function())
