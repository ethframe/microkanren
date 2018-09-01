class Empty:
    def mplus(self, stream):
        return stream

    def bind(self, goal):
        return self


class Cons:
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


class Thunk:
    __slots__ = ("thunk",)

    def __init__(self, thunk):
        self.thunk = thunk

    def mplus(self, stream):
        return Thunk(lambda: stream.mplus(self.thunk()))

    def bind(self, goal):
        return Thunk(lambda: self.thunk().bind(goal))

    def bump(self):
        return self.thunk()


class Deferred:
    __slots__ = ("stream", "goal")

    def __init__(self, stream, goal):
        self.stream = stream
        self.goal = goal

    def mplus(self, stream):
        return Deferred(self.stream.mplus(stream), self.goal)

    def bind(self, goal):
        return self.stream.bind(goal).bind(self.goal)

    def bump(self):
        return self.stream.bind(self.goal)


def iterate(stream):
    while not isinstance(stream, Empty):
        if isinstance(stream, Cons):
            yield stream.head
        stream = stream.bump()
