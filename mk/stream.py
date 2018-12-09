class Stream:
    pass


class Empty(Stream):
    def mplus(self, stream):
        return stream

    def bind(self, goal):
        return self

    def next(self):
        return self


class Cons(Stream):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def mplus(self, stream):
        return Cons(self.head, Thunk(lambda: stream.mplus(self.tail)))

    def bind(self, goal):
        return goal(self.head).mplus(Thunk(lambda: self.tail.bind(goal)))

    def next(self):
        return self.tail


class Cell(Cons):
    def __init__(self, head):
        self.head = head

    def mplus(self, stream):
        return Cons(self.head, stream)

    def bind(self, goal):
        return goal(self.head)

    def next(self):
        return Empty()


class Thunk(Stream):
    __slots__ = ("thunk",)

    def __init__(self, thunk):
        self.thunk = thunk

    def mplus(self, stream):
        return Thunk(lambda: stream.mplus(self.thunk()))

    def bind(self, goal):
        return Thunk(lambda: self.thunk().bind(goal))

    def next(self):
        return self.thunk()


def unfold(stream):
    while type(stream) is not Empty:
        while type(stream) is Thunk:
            stream = stream.next()
        while type(stream) in (Cons, Cell):
            yield stream.head
            stream = stream.next()
