class Stream:
    def defer(self, stream, goal):
        return self.mplus(Deferred(stream, goal))


class Empty(Stream):
    def mplus(self, stream):
        return stream

    def bind(self, goal):
        return self

    def bump(self):
        return self


class Cons(Stream):
    __slots__ = ("head", "tail")

    def __init__(self, head, tail=None):
        self.head = head
        self.tail = Empty() if tail is None else tail

    def mplus(self, stream):
        return Cons(self.head, self.tail.mplus(stream))

    def bind(self, goal):
        return Thunk(lambda: goal(self.head).mplus(self.tail.bind(goal)))

    def bump(self):
        return self.tail


class Thunk(Stream):
    __slots__ = ("thunk",)

    def __init__(self, thunk):
        self.thunk = thunk

    def mplus(self, stream):
        return Thunk(lambda: stream.mplus(self.thunk()))

    def bind(self, goal):
        return Thunk(lambda: self.thunk().bind(goal))

    def bump(self):
        return self.thunk()


class Deferred(Stream):
    __slots__ = ("stream", "goal", "other")

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

    def bump(self):
        return self.other.bump().mplus(self.stream.bind(self.goal))

    def defer(self, stream, goal):
        return Deferred(stream, goal, self)


def iterate(stream):
    while not isinstance(stream, Empty):
        if isinstance(stream, Cons):
            yield stream.head
        stream = stream.bump()
