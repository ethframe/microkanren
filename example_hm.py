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


class If(namedtuple("If", "cond t f")):
    def __repr__(self):
        return "(if {!r} {!r} {!r})".format(*self)


class Let(namedtuple("Let", "id val body")):
    def __repr__(self):
        return "(let ({!r} {!r}) {!r})".format(*self)


class Rec(namedtuple("Rec", "id body")):
    def __repr__(self):
        return "(rec {!r} {!r})".format(*self)


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


TMono = namedtuple("TMono", "type")
TPoly = namedtuple("TPoly", "env body")


@delay
def lookup(o, v, x):
    return fresh(lambda a, b, t: conj(
        eq(o, ((a, b), t)),
        conde(
            [eq(a, v), eq(b, TMono(x))],
            fresh(lambda po, pb, pm: conjp(
                eq(a, v),
                eq(b, TPoly(po, pb)),
                infer(pb, po, x, pm),
            )),
            [neq(a, v), lookup(t, v, x)],
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
            eq(m, App(fa, aa)),
        )),
        fresh(lambda v, vt, b, bt, ba: conjp(
            eq(e, Abs(Sym(v), b)),
            infer(b, ((v, TMono(vt)), o), bt, ba),
            eq(t, TFunc(vt, bt)),
            eq(m, Abs(Ann(Sym(v), vt), ba)),
        )),
        fresh(lambda n, v, b, bm: conjp(
            eq(e, Let(Sym(n), v, b)),
            infer(b, ((n, TPoly(o, v)), o), t, bm),
            eq(m, Let(Sym(n), v, bm)),
        )),
        fresh(lambda n, b, bm: conjp(
            eq(e, Rec(Sym(n), b)),
            infer(b, ((n, TMono(t)), o), t, bm),
            eq(m, Rec(Ann(Sym(n), t), bm)),
        )),
        fresh(lambda c, cm, a, am, b, bm: conjp(
            eq(e, If(c, a, b)),
            infer(c, o, TTerm("bool"), cm),
            infer(a, o, t, am),
            infer(b, o, t, bm),
            eq(m, If(cm, am, bm)),
        )),
        [eqt(e, int), eq(t, TTerm("int")), eq(m, e)],
        [eqt(e, bool), eq(t, TTerm("bool")), eq(m, e)],
    )


def main():
    env = list_to_pair([
        ("+", TMono(TFunc(TTerm("int"), TFunc(TTerm("int"), TTerm("int"))))),
        ("-", TMono(TFunc(TTerm("int"), TFunc(TTerm("int"), TTerm("int"))))),
        ("*", TMono(TFunc(TTerm("int"), TFunc(TTerm("int"), TTerm("int"))))),
        ("==", TMono(TFunc(TTerm("int"), TFunc(TTerm("int"), TTerm("bool"))))),
        ("bool", TMono(TFunc(TTerm("int"), TTerm("bool")))),
    ])
    p = Rec(
        Sym("fac"),
        Abs(
            Sym("n"),
            If(
                App(App(Sym("=="), Sym("n")), 0),
                1,
                App(
                    App(
                        Sym("*"),
                        App(Sym("fac"), App(App(Sym("-"), Sym("n")), 1))
                    ),
                    Sym("n")
                )
            )
        )
    )
    t = Var()
    m = Var()
    print(p)
    for s in run(0, (t, m), infer(p, env, t, m)):
        print(s[0])
        print(s[1])


if __name__ == '__main__':
    main()
