class Stream:
    def defer(self, goal):
        return Deferred(self, goal)


class Empty(Stream):
    def defer(self, goal):
        return self

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
    def __init__(self, thunk):
        self.thunk = thunk

    def mplus(self, stream):
        return Thunk(lambda: stream.mplus(self.thunk()))

    def bind(self, goal):
        return Thunk(lambda: self.thunk().bind(goal))

    def next(self):
        return self.thunk()


class Deferred(Stream):
    def __init__(self, stream, goal):
        self.stream = stream
        self.goal = goal

    def mplus(self, stream):
        return Deferred(Thunk(lambda: self.stream.mplus(stream)), self.goal)

    def bind(self, goal):
        return Thunk(lambda: self.stream.bind(goal).bind(self.goal))

    def next(self):
        return Empty()


def unfold(stream):
    while not isinstance(stream, Empty):
        if isinstance(stream, Cons):
            yield stream.head
        stream = stream.next()
