class Stream:  # pragma: no cover
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
        return Cons(self.head, MPlus(stream, self.tail))

    def bind(self, goal):
        return goal(self.head).mplus(Bind(self.tail, goal))

    def next(self):
        return self.head, self.tail


class ThunkStream(Stream):
    def mplus(self, stream):
        return MPlusThunk(stream, self)

    def bind(self, goal):
        return BindThunk(self, goal)

    def next(self):
        return None, self()


class MPlus(ThunkStream):
    __slots__ = ('left', 'right')

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self):
        return self.left.mplus(self.right)


class Bind(ThunkStream):
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
        return MPlusThunk(stream, self.thunk)

    def bind(self, goal):
        return BindThunk(self.thunk, goal)

    def next(self):
        return None, self.thunk()


class MPlusThunk(ThunkStream):
    __slots__ = ('stream', 'thunk')

    def __init__(self, stream, thunk):
        self.stream = stream
        self.thunk = thunk

    def __call__(self):
        return self.stream.mplus(self.thunk())


class BindThunk(ThunkStream):
    __slots__ = ('thunk', 'goal')

    def __init__(self, thunk, goal):
        self.thunk = thunk
        self.goal = goal

    def __call__(self):
        return self.thunk().bind(self.goal)


class Apply(Stream):
    __slots__ = ('state', 'goal')

    def __init__(self, state, goal):
        self.state = state
        self.goal = goal

    def mplus(self, stream):
        return Apply(self.state, MPlusGoal(stream, self.goal))

    def bind(self, goal):
        return Apply(self.state, BindGoal(self.goal, goal))

    def next(self):
        return None, self.goal(self.state)


class MPlusGoal:
    __slots__ = ('stream', 'goal')

    def __init__(self, stream, goal):
        self.stream = stream
        self.goal = goal

    def __call__(self, state):
        return self.stream.mplus(self.goal(state))


class BindGoal:
    __slots__ = ('left', 'right')

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, state):
        return self.left(state).bind(self.right)


def unfold(stream):
    while stream is not None:
        head, stream = stream.next()
        if head is not None:
            yield head
