class MZero:
    __slots__ = ()

    def mplus(self, stream):
        return stream

    def bind(self, goal):
        return self

    def next(self):
        return None, None


class Unit:
    __slots__ = ('head',)

    def __init__(self, head):
        self.head = head

    def mplus(self, stream):
        return Cons(self.head, stream)

    def bind(self, goal):
        return goal(self.head)

    def next(self):
        return self.head, None


class Cons:
    __slots__ = ('head', 'tail')

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def mplus(self, stream):
        return Cons(self.head, Thunk(lambda: stream.mplus(self.tail)))

    def bind(self, goal):
        return goal(self.head).mplus(Thunk(lambda: self.tail.bind(goal)))

    def next(self):
        return self.head, self.tail


class Thunk:
    __slots__ = ('thunk',)

    def __init__(self, thunk):
        self.thunk = thunk

    def mplus(self, stream):
        return Thunk(lambda: stream.mplus(self.thunk()))

    def bind(self, goal):
        return Thunk(lambda: self.thunk().bind(goal))

    def next(self):
        return None, self.thunk()


def unfold(stream):
    while stream is not None:
        head, stream = stream.next()
        if head is not None:
            yield head
