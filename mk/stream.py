class Stream:
    def mplus(self, stream):
        raise NotImplementedError()

    def bind(self, stream):
        raise NotImplementedError()

    def next(self, stream):
        raise NotImplementedError()


class MZero(Stream):
    __slots__ = ()

    def mplus(self, stream):
        return stream

    def bind(self, goal):
        return self

    def next(self):
        return None, None


class Unit(Stream):
    __slots__ = ('head',)

    def __init__(self, head):
        self.head = head

    def mplus(self, stream):
        return Cons(self.head, stream)

    def bind(self, goal):
        return goal(self.head)

    def next(self):
        return self.head, None


class Cons(Stream):
    __slots__ = ('head', 'tail')

    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def mplus(self, stream):
        return Cons(self.head, Thunk(MPlus(stream, self.tail)))

    def bind(self, goal):
        return goal(self.head).mplus(Thunk(Bind(self.tail, goal)))

    def next(self):
        return self.head, self.tail


class MPlus:
    __slots__ = ('left', 'right')

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self):
        return self.left.mplus(self.right)


class Bind:
    __slots__ = ('stream', 'goal')

    def __init__(self, stream, goal):
        self.stream = stream
        self.goal = goal

    def __call__(self):
        return self.stream.bind(self.goal)


class Thunk(Stream):
    __slots__ = ('thunk',)

    def __init__(self, thunk):
        self.thunk = thunk

    def mplus(self, stream):
        return Thunk(MPlusThunk(stream, self.thunk))

    def bind(self, goal):
        return Thunk(BindThunk(self.thunk, goal))

    def next(self):
        return None, self.thunk()


class MPlusThunk:
    __slots__ = ('stream', 'thunk')

    def __init__(self, stream, thunk):
        self.stream = stream
        self.thunk = thunk

    def __call__(self):
        return self.stream.mplus(self.thunk())


class BindThunk:
    __slots__ = ('thunk', 'goal')

    def __init__(self, thunk, goal):
        self.thunk = thunk
        self.goal = goal

    def __call__(self):
        return self.thunk().bind(self.goal)


def unfold(stream):
    while stream is not None:
        head, stream = stream.next()
        if head is not None:
            yield head
