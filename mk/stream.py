class Stream:
    def defer(self, stream, goal):
        return self.mplus(Deferred(stream, goal))


class Empty(Stream):
    def mplus(self, stream):
        return stream

    def bind(self, goal):
        return self

    def next(self):
        return self


class Cons(Stream):
    def __init__(self, head, tail=None):
        self.head = head
        self.tail = Empty() if tail is None else tail

    def mplus(self, stream):
        return Cons(self.head, stream.mplus(self.tail))

    def bind(self, goal):
        return Thunk(lambda: goal(self.head).mplus(self.tail.bind(goal)))

    def next(self):
        return self.tail


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
    def __init__(self, stream, goal, other=None):
        self.stream = stream
        self.goal = goal
        self.other = Empty() if other is None else other

    def mplus(self, stream):
        return self.other.mplus(stream).defer(self.stream, self.goal)

    def bind(self, goal):
        return self.other.bind(goal).mplus(
            self.stream.bind(goal).bind(self.goal)
        )

    def next(self):
        return self.other.next().mplus(self.stream.bind(self.goal))

    def defer(self, stream, goal):
        return Deferred(stream, goal, self)


def unfold(stream):
    while not isinstance(stream, Empty):
        if isinstance(stream, Cons):
            yield stream.head
        stream = stream.next()
