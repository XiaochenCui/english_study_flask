class Queue(object):
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def en_queue(self, item):
        self.items.insert(0,item)

    def de_queue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


if __name__ == '__main__':
    q = Queue()
    q.en_queue(4)
    q.en_queue('dog')
    q.en_queue(True)
    print(q.size())
    print(q.de_queue())
    print(q.size())