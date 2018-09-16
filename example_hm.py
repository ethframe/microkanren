from collections import namedtuple

from mk.core import conj, eq, eqt
from mk.disequality import neq
from mk.ext import conde, conjp, delay, fresh
from mk.list import list_to_pair
from mk.run import run
from mk.unify import Var


class Abs(namedtuple("Abs", "arg body")):
    def __repr__(self):
        return "(lambda {!r} {!r})".format(*self)


class App(namedtuple("App", "fn arg")):
    def __repr__(self):
        return "({!r} {!r})".format(*self)


class Sym(namedtuple("Sym", "name")):
    def __repr__(self):
        return str(self.name)


class Ann(namedtuple("Ann", "term type")):
    def __repr__(self):
        return "{!r}:{!r}".format(*self)


class TFunc(namedtuple("TFunc", "arg res")):
    def __repr__(self):
        return "({!r} -> {!r})".format(*self)


class TTerm(namedtuple("TTerm", "name")):
    def __repr__(self):
        return str(self.name)


@delay
def lookup(o, v, x):
    return fresh(lambda a, b, t: conj(
        eq(o, ((a, b), t)),
        conde(
            [eq(a, v), eq(b, x)],
            [neq(a, v), lookup(t, v, x)]
        )
    ))


@delay
def infer(e, o, t, m):
    return conde(
        fresh(lambda n: conjp(
            eq(e, Sym(n)),
            lookup(o, n, t),
            eq(m, Ann(e, t)),
        )),
        fresh(lambda f, ft, fa, a, at, aa: conjp(
            eq(e, App(f, a)),
            infer(a, o, at, aa),
            infer(f, o, TFunc(at, t), fa),
            eq(m, Ann(App(fa, aa), t)),
        )),
        fresh(lambda v, vt, b, bt, ba: conjp(
            eq(e, Abs(Sym(v), b)),
            infer(b, ((v, vt), o), bt, ba),
            eq(t, TFunc(vt, bt)),
            eq(m, Abs(Ann(Sym(v), vt), ba)),
        )),
        [eqt(e, int), eq(t, TTerm("int")), eq(m, Ann(e, t))],
        [eqt(e, bool), eq(t, TTerm("bool")), eq(m, Ann(e, t))],
    )


def main():
    env = list_to_pair([
        ("+", TFunc(TTerm("int"), TFunc(TTerm("int"), TTerm("int")))),
        ("bool", TFunc(TTerm("int"), TTerm("bool"))),
    ])
    p = App(
        Abs(
            Sym("id"),
            Abs(Sym("v"), App(Sym("id"), App(Sym("bool"), Sym("v")))),
        ),
        Abs(Sym("x"), Sym("x")),
    )
    t = Var()
    m = Var()
    for s in run(0, (t, m), infer(p, env, t, m)):
        print(s[0])
        print(s[1])


if __name__ == '__main__':
    main()
