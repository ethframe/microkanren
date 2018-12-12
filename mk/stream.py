class MZero:
    def mplus(self, stream):
        return stream

    def bind(self, goal):
        return self

    def next(self):
        return self


class Cons:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def mplus(self, stream):
        return Cons(self.head, Thunk(lambda: stream.mplus(self.tail)))

    def bind(self, goal):
        return goal(self.head).mplus(Thunk(lambda: self.tail.bind(goal)))

    def next(self):
        return self.tail


class Unit:
    def __init__(self, head):
        self.head = head

    def mplus(self, stream):
        return Cons(self.head, stream)

    def bind(self, goal):
        return goal(self.head)

    def next(self):
        return MZero()


class Thunk:
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
    while type(stream) is not MZero:
        while type(stream) is Thunk:
            stream = stream.next()
        while type(stream) in (Cons, Unit):
            yield stream.head
            stream = stream.next()
